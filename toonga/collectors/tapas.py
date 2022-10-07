from abc import ABC

from .Base import BaseClient, Series, Chapter, SeriesDetails


class Client(BaseClient, ABC):
    name = "Tapas"

    def __init__(self, user=None, password=None, api_url=None):
        super().__init__(user, password, api_url or "https://tapas.io")
        self.s.headers.update({"user-agent": "toonga-tapas-info-grabber"})
        self.base_website = "https://tapas.io"

    def search_series(self, search_string):
        r = self.s.get(self.api_url + "/search/summary", params={"query": search_string})
        self.check_response(r)
        data = r.json()
        series_ids = self.get_all(data["data"]["body"], r'data-series-id="(\d+)"')
        series_urls = self.get_all(data["data"]["body"], r'data-on-sale="\w+"\s+href="(.*?)"')
        if len(series_ids) != len(series_urls):
            raise Exception("Failed to extract data from page")
        return [Series(id=i, url=self.base_website + u, name=u.split("/")[-1]) for i, u in zip(series_ids, series_urls)]

    def get_series(self, series: Series):
        r = self.s.get(f"{self.api_url}/series/{series.id}/event-properties",
                       params={"fields": "series_title,total_episode_number"})
        self.check_response(r)
        data = r.json()
        series.name = data["data"]["body"]["series_title"]
        return series

    def get_chapters(self, series: Series):
        r = self.s.get(f"{self.api_url}/series/{series.id}/episodes", params={"sort": "NEWEST"})
        self.check_response(r)
        data = r.json()
        if not series.details:
            series.details = SeriesDetails()
        series.add_chapters([Chapter(num=i) for i in self.get_all(data["data"]["body"], r"Episode (\d+)")])
        return series.details.chapters


if __name__ == "__main__":
    c = Client()

    all_series = c.search_series("After the End")
    serie = all_series[0]
    print(serie)
    serie = c.get_series(serie)
    print(serie)
    all_chapters = c.get_chapters(serie)
    print(all_chapters)

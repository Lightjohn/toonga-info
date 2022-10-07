from typing import List

from .Base import BaseClient, Series, Chapter, SeriesDetails, MatchException


class Client(BaseClient):
    name = "Webtoon"

    def __init__(self, user=None, password=None, api_url=None):
        super().__init__(user, password, api_url or "https://ac.webtoons.com")
        self.s.headers.update({"user-agent": "toonga-webtoon-info-grabber"})

    def search_series(self, search_string: str) -> List[Series]:
        params = {
            "q": f"en^{search_string}",
            "q_enc": "UTF-8",
            "st": 1,  # IMPORTANT
            "r_lt": 0,
            "r_format": "json",
            "r_enc": "UTF-8",
        }
        r = self.s.get(self.api_url + "/ac", params=params)
        self.check_response(r)
        data = r.json()
        return [Series(name=i[0][0], id=i[3][0]) for i in data["items"][0]]

    def get_series(self, series: Series) -> Series:
        r = self.s.get(
            f"https://www.webtoons.com/episodeList?titleNo={series.id}"
        )  # Will generate a 301 to good url
        self.check_response(r)
        series.url = r.url
        summary = self.get_first(r.text, r'<p class="summary">(.*?)</p>')
        chapters = None
        for reg in ["Episode", "Ep."]:
            try:
                chapters = self.get_all(r.text, rf"{reg} (\d+)")
                break
            except MatchException:
                pass
        if not chapters or not summary:
            raise Exception("Could not get chapters")
        series.details = SeriesDetails(summary=summary,
                                       chapters=[Chapter(num=i) for i in chapters])
        return series

    def get_chapters(self, series: Series) -> List[Chapter]:
        # Just getting series will populate chapters
        if not series.details or not series.details.chapters:
            self.get_series(series)
        return series.details.chapters


if __name__ == "__main__":
    c = Client()
    all_series = c.search_series("love")
    serie = all_series[0]
    print(serie.name, serie.name)

    s = c.get_series(serie)
    print(s)
    print(s.details.chapters)

from .Base import BaseClient, Series, SeriesDetails, Chapter


class Client(BaseClient):
    name = "Mangaupdate"

    def __init__(self, user=None, password=None, api_url=None):
        super().__init__(user, password, api_url or "https://api.mangaupdates.com/v1")

    def login(self, user, password):
        r = self.s.put(
            self.api_url + "/account/login",
            json={"username": user, "password": password},
        )
        self.check_response(r)
        data = r.json()
        if "success" != data["status"]:
            raise Exception("Failed to login", data["reason"])
        return data["context"]["session_token"]

    def search_series(self, search_string):
        r = self.s.post(self.api_url + "/series/search", json={"search": search_string})
        self.check_response(r)
        data = r.json()
        return [Series(name=i["record"]["title"],
                       id=i["record"]["series_id"],
                       url=i["record"]["url"]) for i in data["results"]]

    def get_series(self, series: Series):
        r = self.s.get(self.api_url + f"/series/{series.id}")
        self.check_response(r)
        data = r.json()
        last_chapter = Chapter(num=data["latest_chapter"])

        series.details = SeriesDetails(summary=data["description"],
                                       chapters=[last_chapter],
                                       other_titles=[list(i.values())[0] for i in data["associated"]])
        return series

    def get_chapters(self, series: Series):
        # No way to found chapters so using existing methods
        if not series.details or not series.details.chapters:
            self.get_series(series)
        return series.details.chapters

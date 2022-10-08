from typing import List

from .Base import BaseClient, Series, Chapter, SeriesDetails


class Client(BaseClient):
    name = "Mangadex"

    def __init__(self, user=None, password=None, api_url=None):
        super().__init__(user, password, api_url or "https://api.mangadex.org")

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

    def search_series(self, search_string) -> List[Series]:
        r = self.s.get(self.api_url + "/manga", params={"title": search_string})
        self.check_response(r)
        data = r.json()
        return_series = []
        for series_data in data["data"]:
            if "en" in series_data["attributes"]["title"]:
                name = series_data["attributes"]["title"]["en"]
            else:
                name = next(iter(series_data["attributes"]["title"].values()))
            series = Series(name=name, id=series_data["id"])
            return_series.append(series)
        return return_series

    def get_series(self, series: Series) -> Series:
        r = self.s.get(self.api_url + f"/manga/{series.id}")
        self.check_response(r)
        data = r.json()["data"]
        attributes = data["attributes"]
        details = SeriesDetails(summary=attributes["description"]["en"],
                                other_titles=[list(i.values())[0] for i in attributes["altTitles"]])
        url = attributes["links"]["engtl"] if attributes["links"] and "engtl" in attributes["links"] else ""
        series.name = attributes["title"]["en"]
        series.id = data["id"]
        series.details = details
        series.url = url
        return series

    def get_chapters(self, series: Series) -> List[Chapter]:
        r = self.s.get(self.api_url + f"/manga/{series.id}/aggregate")
        self.check_response(r)
        s = r.json()
        if "volumes" in s and s["volumes"]:
            volumes = s["volumes"].values()
            chapters = []
            [chapters.extend(volume["chapters"].values()) for volume in volumes]
        elif "chapters" in s:
            chapters = s["chapters"]
        else:
            chapters = []
        for chap in chapters:  # Sometime None can be found as chapter number so cleaning here
            try:
                float(chap["chapter"])
            except ValueError:
                chapters.remove(chap)
        series.add_chapters([Chapter(num=chapter["chapter"], id=chapter["id"]) for chapter in chapters])
        return series.details.chapters

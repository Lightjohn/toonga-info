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
        return [Series(name=s["attributes"]["title"]["en"], id=s["id"]) for s in data["data"]]

    def get_series(self, series: Series) -> Series:
        r = self.s.get(self.api_url + f"/manga/{series.id}")
        self.check_response(r)
        data = r.json()["data"]
        attributes = data["attributes"]
        details = SeriesDetails(summary=attributes["description"]["en"],
                                other_titles=[list(i.values())[0] for i in attributes["altTitles"]])
        url = attributes["links"]["engtl"] if "engtl" in attributes["links"] else ""
        series.name = attributes["title"]["en"]
        series.id = data["id"]
        series.details = details
        return series

    def get_chapters(self, series: Series) -> List[Chapter]:
        r = self.s.get(self.api_url + f"/manga/{series.id}/aggregate")
        self.check_response(r)
        s = r.json()
        if "volumes" in s:
            volumes = s["volumes"].values()
            chapters = []
            [chapters.extend(volume["chapters"].values()) for volume in volumes]
        else:
            chapters = s["chapters"]
        series.add_chapters([Chapter(num=chapter["chapter"], id=chapter["id"]) for chapter in chapters])
        return series.details.chapters


if __name__ == "__main__":
    c = Client()
    all_series = c.search_series("I’ll Be The Matriarch In This Life")
    serie = all_series[0]
    print(serie.name, serie.id)

    s = c.get_series(serie)
    print(s)

    all_chapters = c.get_chapters(serie)

    print("Last chapter (chapters)", [int(c.num) for c in all_chapters])

import re
from abc import ABC
from typing import List

import requests

from .Base import BaseClient, Series, Chapter


class Client(BaseClient):
    name = "Tappytoon"

    def __init__(self, user=None, password=None, api_url=None):
        super().__init__(user, password, api_url or "https://api-global.tappytoon.com")
        self.web_url = "https://www.tappytoon.com/"
        self.s.headers.update(
            {
                "user-agent": "tappytoon-info-grabber",
                "Origin": self.web_url,
                "Referer": self.web_url,
            }
        )
        self.login()

    def login(self, user=None, password=None):
        # grab Bearer token
        r = self.s.get(self.web_url)
        self.check_response(r)
        token = self.get_first(r.text, r'"Bearer (.*?)"')
        self.s.headers.update(
            {"Host": "api-global.tappytoon.com", "Authorization": f"Bearer {token}"}
        )

    def search_series(self, search_string: str) -> List[Series]:
        params = {
            "excludes": "wait_until_free_next_id",
            "category": "comic",
            "locale": "en",
            "keyword": search_string,
        }

        r = self.s.get(self.api_url + "/comics", params=params)
        self.check_response(r)
        return [Series(name=i["title"], id=i["id"], url=self.web_url + "comics/" + i["slug"]) for i in r.json()]

    def get_series(self, series: Series) -> Series:
        if series.name and series.url:
            return series  # Already complete
        r = self.s.get(f"{self.api_url}/comics/{series.id}")
        self.check_response(r)
        data = r.json()
        series.name = data["title"]
        series.url = self.web_url + "comics/" + data["slug"]
        series.add_summary(data["longDescription"])
        return series

    def get_chapters(self, series: Series) -> List[Chapter]:
        r = self.s.get(f"{self.api_url}/comics/{series.id}/chapters", params={"sort": "desc"})
        self.check_response(r)
        data = r.json()
        series.add_chapters([Chapter(id=i["id"], num=i["order"]) for i in data])
        return series.details.chapters

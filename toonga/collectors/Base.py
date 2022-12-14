import re
from dataclasses import dataclass
from typing import List

import requests
from requests import Response
from requests.adapters import HTTPAdapter, Retry


@dataclass
class Chapter:
    num: str
    id: str = ""


@dataclass
class SeriesDetails:
    summary: str = ""
    chapters: List[Chapter] = None
    other_titles: List[str] = None


@dataclass
class Series:
    id: str
    name: str = ""
    url: str = ""
    details: SeriesDetails = None

    def add_chapters(self, chapters: List[Chapter]):
        if not self.details:
            self.details = SeriesDetails()
        self.details.chapters = chapters

    def add_summary(self, summary: str):
        if not self.details:
            self.details = SeriesDetails()
        self.details.summary = summary

    def add_titles(self, titles: List[str]):
        if not self.details:
            self.details = SeriesDetails()
        self.details.other_titles = titles


class MatchException(Exception):
    pass


class BaseClient:
    name = "Default"

    def __init__(self, user=None, password=None, api_url=None):
        self.s = requests.Session()
        retries = Retry(total=2, backoff_factor=0.5)
        self.s.mount('https://', HTTPAdapter(max_retries=retries))
        self.api_url = api_url
        if user and password:
            self.login(user, password)

    def login(self, user, password):
        raise NotImplementedError

    @staticmethod
    def check_response(r: Response):
        if r.ok:
            return
        if 400 <= r.status_code < 500:
            raise Exception("Oups forbidden, auth seems to have failed", r.status_code)
        if r.status_code >= 500:
            raise Exception("Oups broke api", r.status_code, r.json())

    @staticmethod
    def get_first(body: str, pattern: str):
        m = re.search(pattern, body.replace("\n", ""))
        results = m.groups()
        if not results:
            return results
        return results[0]

    @staticmethod
    def get_all(body: str, pattern: str):
        results = re.findall(pattern, body)
        return results

    def search_series(self, search_string: str) -> List[Series]:
        raise NotImplementedError

    def get_series(self, series: Series) -> Series:
        raise NotImplementedError

    def get_chapters(self, series: Series) -> List[Chapter]:
        raise NotImplementedError

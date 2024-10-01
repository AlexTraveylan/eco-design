from functools import cached_property

import requests

from app.adapter.exception.app_exception import AppError
from app.core.insight.interface import Insight, InsightContent, endpoint
from app.core.settings import SETTINGS


class GoogleInsight(Insight):
    """
    Attributes
    ----------
    url : str
        The URL to test

    Methods
    -------
    load() -> dict:
        Load the insights from the Google API
    get_desktop_result() -> InsightContent:
        Get the insights for the desktop version
    get_mobile_result() -> InsightContent:
        Get the insights for the mobile version
    """

    def __init__(self, url: str, strategy: str) -> None:
        self.url = url
        self.strategy = strategy
        self._api_key = SETTINGS.GOOGLE_INSIGHTS_API_KEY

    @cached_property
    def load(self) -> dict:
        api_url = endpoint(self.url, self.api_key)

        response = requests.get(api_url)

        if response.status_code == 200:
            return response.json()
        else:
            raise AppError(f"Erreur {response.status_code}: {response.text}")

    def get_desktop_result(self) -> InsightContent:
        pass

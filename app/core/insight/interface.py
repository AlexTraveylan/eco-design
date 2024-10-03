from abc import ABC
from collections.abc import Iterable
from functools import cached_property
from typing import Literal

import requests
from pydantic import BaseModel

from app.adapter.exception.app_exception import GoogleInsightError, ParsingError
from app.core.settings import SETTINGS


class InsightContent(BaseModel):
    """
    Attributes
    ----------
    performance : int
        Score 0-100
    accessibility : int
        Score 0-100
    best_practices : int
        Score 0-100
    seo : int
        Score 0-100
    first_contentful_paint : int
    largest_contentful_paint : int
    total_blocking_time : int
    cumulative_layout_shift : float
    speed_index : int
    """

    performance: int
    accessibility: int
    best_practices: int
    seo: int
    first_contentful_paint: int
    largest_contentful_paint: int
    total_blocking_time: int
    cumulative_layout_shift: float
    speed_index: int


Strategy = Literal["mobile", "desktop"]
Category = Literal["accessibility", "performance", "best_practices", "seo"]
Locale = Literal["fr", "en"]

ALL_CATEGORIES = "accessibility", "performance", "best_practices", "seo"


def endpoint(
    *,
    url: str,
    api_key: str,
    strategy: Strategy,
    categories: Iterable[Category] | None = None,
    locale: Locale = "fr",
) -> str:
    # Default categories
    categories = categories or ALL_CATEGORIES

    # Base URL
    base_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"

    # Add the URL to the base URL
    base_url += f"url={url}"

    # Add the categories to the base URL
    for category in categories:
        base_url += f"&category={category}"

    # Add the API key to the base URL
    base_url += f"&key={api_key}"

    # Add the strategy to the base URL
    base_url += f"&strategy={strategy}"

    # Add the locale to the base URL
    base_url += f"&locale={locale}"

    return base_url


def get_insight_or_raise(data: dict, key: str) -> dict | int | str | float:
    result = data.get(key)

    if result is None:
        raise ParsingError(f"Cannot find {key} on insight result")

    return result


class Insight(ABC):
    _STATEGY: Strategy

    def __init__(self, url: str, *, locale: Locale = "fr") -> None:
        self.url = url
        self.locale = locale

    def get_result(self) -> InsightContent:
        return InsightContent(
            performance=int(self.performance["score"] * 100),
            accessibility=int(self.accessibility["score"] * 100),
            best_practices=int(self.best_practices["score"] * 100),
            seo=int(self.seo["score"] * 100),
            cumulative_layout_shift=self.cumulative_layout_shift,
            first_contentful_paint=self.first_contentful_paint,
            speed_index=self.speed_index,
            largest_contentful_paint=self.largest_contentful_paint,
            total_blocking_time=self.total_blocking_time,
        )

    @cached_property
    def data(self) -> dict:
        api_url = endpoint(
            url=self.url,
            api_key=SETTINGS.GOOGLE_INSIGHTS_API_KEY,
            categories=ALL_CATEGORIES,
            strategy=self._STATEGY,
            locale=self.locale,
        )

        response = requests.get(api_url)

        if response.status_code != 200:
            raise GoogleInsightError(f"Erreur {response.status_code}: {response.text}")

        return response.json()

    @cached_property
    def _light_result(self) -> dict:
        return get_insight_or_raise(self.data, "lighthouseResult")

    @cached_property
    def _categories(self) -> dict:
        return get_insight_or_raise(self._light_result, "categories")

    @property
    def performance(self) -> dict:
        return get_insight_or_raise(self._categories, "performance")

    @property
    def accessibility(self) -> dict:
        return get_insight_or_raise(self._categories, "accessibility")

    @property
    def best_practices(self) -> dict:
        return get_insight_or_raise(self._categories, "best-practices")

    @property
    def seo(self) -> dict:
        return get_insight_or_raise(self._categories, "seo")

    @cached_property
    def _audits(self) -> dict:
        return get_insight_or_raise(self._light_result, "audits")

    @cached_property
    def _metrics(self) -> dict:
        return get_insight_or_raise(self._audits, "metrics")

    @cached_property
    def _details(self) -> dict:
        return get_insight_or_raise(self._metrics, "details")

    @cached_property
    def _details_items(self) -> dict:
        return get_insight_or_raise(self._details, "items")[0]

    @property
    def cumulative_layout_shift(self) -> float:
        return get_insight_or_raise(self._details_items, "cumulativeLayoutShift")

    @property
    def first_contentful_paint(self) -> int:
        return get_insight_or_raise(self._details_items, "firstContentfulPaint")

    @property
    def speed_index(self) -> int:
        return get_insight_or_raise(self._details_items, "speedIndex")

    @property
    def largest_contentful_paint(self) -> int:
        return get_insight_or_raise(self._details_items, "largestContentfulPaint")

    @property
    def total_blocking_time(self) -> int:
        return get_insight_or_raise(self._details_items, "totalBlockingTime")

    @property
    def time_to_first_byte(self) -> int:
        return get_insight_or_raise(self._details_items, "timeToFirstByte")

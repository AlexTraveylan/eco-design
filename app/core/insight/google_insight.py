from abc import ABC
from functools import cached_property

import requests

from app.adapter.exception.app_exception import GoogleInsightError
from app.core.insight.schemas import (
    ALL_CATEGORIES,
    InsightContent,
    Locale,
    Strategy,
)
from app.core.insight.tools import endpoint, get_insight_or_raise
from app.core.settings import SETTINGS


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


class MobileInsight(Insight):
    _STATEGY = "mobile"


class DestopInsight(Insight):
    _STATEGY = "desktop"

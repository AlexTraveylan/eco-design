from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Literal

from pydantic import BaseModel


class InsightContent(BaseModel):
    """
    Attributes
    ----------
    performance : int
    accessibility : int
    best_practices : int
    seo : int
    first_contentful_paint : float
    largest_contentful_paint : float
    total_blocking_time : int
    cumulative_layout_shift : float
    speed_index : float
    """

    performance: int
    accessibility: int
    best_practices: int
    seo: int
    first_contentful_paint: float
    largest_contentful_paint: float
    total_blocking_time: int
    cumulative_layout_shift: float
    speed_index: float


Strategy = Literal["mobile", "desktop"]
Category = Literal["accessibility", "performance", "best_practices", "seo"]
Locale = Literal["fr", "en"]


def endpoint(
    *,
    url: str,
    api_key: str,
    strategy: Strategy,
    categories: Iterable[Category] | None = None,
    locale: Locale = "fr",
) -> str:
    # Default categories
    categories = categories or ("accessibility", "performance", "best_practices", "seo")

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


class Insight(ABC):
    @abstractmethod
    def load(self, url: str, strategy: Strategy) -> dict:
        pass

    @abstractmethod
    def get_result(self) -> InsightContent:
        pass

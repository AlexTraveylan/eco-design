from typing import Literal

from pydantic import BaseModel


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
        Unit : ms
    largest_contentful_paint : int
        Unit : ms
    total_blocking_time : int
        Unit : ms
    cumulative_layout_shift : float
    speed_index : int
        Unit : ms
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

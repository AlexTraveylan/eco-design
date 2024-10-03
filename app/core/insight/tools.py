from collections.abc import Iterable

from app.adapter.exception.app_exception import ParsingError
from app.core.insight.schemas import (
    ALL_CATEGORIES,
    Category,
    Locale,
    Strategy,
)


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

"""
Main module for the application
"""

import asyncio
import logging
from atexit import register

from app.core.constants import LOGGER_NAME
from app.core.eco_index.scraper import EcoindexScraper
from app.core.insight.google_insight import MobileInsight

logger = logging.getLogger(LOGGER_NAME)


def main():
    """Entry point for the application."""
    url = "https://www.alextraveylan.fr"
    insight = MobileInsight(url)
    print(insight.get_result())

    eco_index = asyncio.run(EcoindexScraper(url=url).get_page_analysis())
    print(eco_index)


@register
def exit_function():
    """Auto execute when application end"""

    logger.info("application ended")


if __name__ == "__main__":
    main()

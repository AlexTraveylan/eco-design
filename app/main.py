"""
Main module for the application
"""

import logging
from atexit import register

import requests

from app.core.constants import LOGGER_NAME
from app.core.settings import SETTINGS

logger = logging.getLogger(LOGGER_NAME)


def main():
    """Entry point for the application."""
    API_KEY = SETTINGS.GOOGLE_INSIGHTS_API_KEY

    url = "https://www.alextraveylan.fr"
    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&key={API_KEY}"

    response = requests.get(api_url)

    # Vérifier si la requête s'est bien déroulée
    if response.status_code == 200:
        json_response = response.json()
        print(json_response)
    else:
        print(f"Erreur {response.status_code}: {response.text}")


@register
def exit_function():
    """Auto execute when application end"""

    logger.info("application ended")


if __name__ == "__main__":
    main()

from playwright.sync_api import sync_playwright

from app.adapter.exception.app_exception import AnalyseMustBeDoneFirstError
from app.core.inspect_network.schemas import NetworkRequest


class InspectNetWork:
    def __init__(self, url: str) -> None:
        self.url = url
        self._total_requests: int = 0
        self._js_requests: int = 0
        self._css_requests: int = 0
        self._is_analysed: bool = False

    def analyse(self) -> None:
        if self._is_analysed is True:
            return

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.on("request", self._handle_request)

            page.goto(self.url)

            page.wait_for_load_state("networkidle")

            browser.close()

        self._is_analysed = True

    def get_result(self) -> NetworkRequest:
        if self._is_analysed is False:
            raise AnalyseMustBeDoneFirstError("use InspectNetWork.analyse() before")

        return NetworkRequest(
            total=self._total_requests,
            js=self._js_requests,
            css=self._css_requests,
        )

    def _handle_request(self, request):
        self._total_requests += 1

        if request.resource_type == "script":
            self._js_requests += 1
        elif request.resource_type == "stylesheet":
            self._css_requests += 1


# Exemple d'utilisation
url_to_analyze = "https://www.francetravail.fr/accueil"
inpect = InspectNetWork(url=url_to_analyze)
inpect.analyse()
print(inpect.get_result())

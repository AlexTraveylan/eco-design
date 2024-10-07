import asyncio

import rich
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from app.core.eco_index.scraper import EcoindexScraper
from app.core.insight.google_insight import DestopInsight, MobileInsight
from app.core.insight.schemas import InsightContent
from app.core.inspect_network.count_requests import InspectNetWork
from app.usecase.excel_completion.actions import (
    create_excel_from_template,
    open_excel_file,
)
from app.usecase.excel_completion.files_infos import (
    TEMPLATE_PATH,
    get_output_path,
)

app = typer.Typer()


@app.command()
def insight(url: str, strategy: str):
    if strategy == "desktop":
        insight_class = DestopInsight(url)

    elif strategy == "mobile":
        insight_class = MobileInsight(url)

    else:
        print("Stategy must be desktop or mobile")
        raise typer.Exit()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data ...", total=None)
        result: InsightContent = insight_class.get_result()

    rich.print(result.model_dump())


@app.command()
def eco_index(url: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data ...", total=None)
        eco_index = asyncio.run(EcoindexScraper(url=url).get_page_analysis())

    rich.print(eco_index.model_dump())


@app.command()
def network(url: str):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data ...", total=None)
        inspect = InspectNetWork(url=url).get_result()

    rich.print(inspect.model_dump())


@app.command()
def complete_excel(urls: list[str]):
    output_path = get_output_path()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data ...", total=None)
        create_excel_from_template(TEMPLATE_PATH, output_path, urls)
        open_excel_file(output_path)


if __name__ == "__main__":
    app()

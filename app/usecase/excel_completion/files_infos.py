from datetime import datetime
from pathlib import Path

from app.adapter.exception.app_exception import AppError

DATA_FOLDER = Path(__file__).parent / "data"

TEMPLATE_PATH = DATA_FOLDER / "template.xlsx"

OUTPUT_FOLDER = DATA_FOLDER / "output"
if OUTPUT_FOLDER.exists() is False:
    OUTPUT_FOLDER.mkdir()

SYNTHESE_PAGE_NAME = "Synthèse"

LIST_PAGE_NAME = "Liste"


def get_output_path() -> Path:
    if OUTPUT_FOLDER is False:
        raise AppError(f"Le dossier {OUTPUT_FOLDER} n'existe pas")

    return OUTPUT_FOLDER / f"DIAG_Ecoconception_{datetime.now().timestamp()}.xlsx"

from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, Field, field_validator


class Grade(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"


class Ecoindex(BaseModel):
    grade: Grade | None = Field(
        default=None,
        title="Ecoindex grade",
        description="Is the corresponding ecoindex grade of the page (from A to G)",
    )
    score: float | None = Field(
        default=None,
        title="Ecoindex score",
        description="Is the corresponding ecoindex score of the page (0 to 100)",
        ge=0,
        le=100,
    )
    ges: float | None = Field(
        default=None,
        title="Ecoindex GES equivalent",
        description=(
            "Is the equivalent of greenhouse gases emission" " (in `gCO2e`) of the page"
        ),
        ge=0,
    )
    water: float | None = Field(
        default=None,
        title="Ecoindex Water equivalent",
        description="Is the equivalent water consumption (in `cl`) of the page",
        ge=0,
    )


class WindowSize(BaseModel):
    height: int = Field(
        default=...,
        title="Window height",
        description="Height of the simulated window in pixel",
    )
    width: int = Field(
        default=...,
        title="Window width",
        description="Width of the simulated window in pixel",
    )

    def __str__(self) -> str:
        return f"{self.width},{self.height}"


class ScreenShot(BaseModel):
    id: str
    folder: str

    def __init__(__pydantic_self__, **data) -> None:
        super().__init__(**data)
        path = Path(__pydantic_self__.folder)
        path.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        return f"{self.folder}/{self.id}"

    def get_png(self) -> str:
        return f"{self.__str__()}.png"

    def get_webp(self) -> str:
        return f"{self.__str__()}.webp"


class Request(BaseModel):
    url: str
    type: str
    size: float


class RequestItem(BaseModel):
    category: str
    mime_type: str
    size: float
    status: int
    url: str


class MimetypeMetrics(BaseModel):
    total_count: int = 0
    total_size: float = 0


class MimetypeAggregation(BaseModel):
    audio: MimetypeMetrics = MimetypeMetrics()
    css: MimetypeMetrics = MimetypeMetrics()
    font: MimetypeMetrics = MimetypeMetrics()
    html: MimetypeMetrics = MimetypeMetrics()
    image: MimetypeMetrics = MimetypeMetrics()
    javascript: MimetypeMetrics = MimetypeMetrics()
    other: MimetypeMetrics = MimetypeMetrics()
    video: MimetypeMetrics = MimetypeMetrics()

    @classmethod
    async def get_category_of_resource(cls, mimetype: str) -> str:
        mimetypes = [type for type in cls.model_fields.keys()]

        for type in mimetypes:
            if type in mimetype:
                return type

        return "other"


class Requests(BaseModel):
    aggregation: MimetypeAggregation = MimetypeAggregation()
    items: list[RequestItem] = []
    total_count: int = 0
    total_size: float = 0


class PageMetrics(BaseModel):
    size: float = Field(
        default=...,
        title="Page size",
        description=(
            "Is the size of the page and of the downloaded"
            " elements of the page in KB"
        ),
        ge=0,
    )
    nodes: int = Field(
        default=...,
        title="Page nodes",
        description="Is the number of the DOM elements in the page",
        ge=0,
    )
    requests: int = Field(
        default=...,
        title="Page requests",
        description="Is the number of external requests made by the page",
        ge=0,
    )


class WebPage(BaseModel):
    width: int | None = Field(
        default=1920,
        title="Page Width",
        description="Width of the simulated window in pixel",
        ge=100,
        le=3840,
    )
    height: int | None = Field(
        default=1080,
        title="Page Height",
        description="Height of the simulated window in pixel",
        ge=50,
        le=2160,
    )
    url: str = Field(
        default=...,
        title="Page url",
        description="Url of the analysed page",
        examples=["https://www.ecoindex.fr"],
    )

    @field_validator("url")
    @classmethod
    def url_as_http_url(cls, v: str) -> str:
        url_object = AnyHttpUrl(url=v)
        assert url_object.scheme in {"http", "https"}, "scheme must be http or https"

        return url_object.unicode_string()

    def get_url_host(self) -> str:
        url_object = AnyHttpUrl(url=self.url)

        return str(url_object.host)

    def get_url_path(self) -> str:
        url_obect = AnyHttpUrl(url=self.url)

        return str(url_obect.path)


PageType = str


class Result(Ecoindex, PageMetrics, WebPage):
    date: datetime | None = Field(
        default=None, title="Analysis datetime", description="Date of the analysis"
    )
    page_type: PageType | None = Field(
        default=None,
        title="Page type",
        description="Is the type of the page, based ton the [opengraph type tag](https://ogp.me/#types)",
    )


quantiles_dom = [
    0,
    47,
    75,
    159,
    233,
    298,
    358,
    417,
    476,
    537,
    603,
    674,
    753,
    843,
    949,
    1076,
    1237,
    1459,
    1801,
    2479,
    594601,
]
quantiles_req = [
    0,
    2,
    15,
    25,
    34,
    42,
    49,
    56,
    63,
    70,
    78,
    86,
    95,
    105,
    117,
    130,
    147,
    170,
    205,
    281,
    3920,
]
quantiles_size = [
    0,
    1.37,
    144.7,
    319.53,
    479.46,
    631.97,
    783.38,
    937.91,
    1098.62,
    1265.47,
    1448.32,
    1648.27,
    1876.08,
    2142.06,
    2465.37,
    2866.31,
    3401.59,
    4155.73,
    5400.08,
    8037.54,
    223212.26,
]

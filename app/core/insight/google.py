from app.core.insight.interface import (
    Insight,
)


class MobileInsight(Insight):
    _STATEGY = "mobile"


class DestopInsight(Insight):
    _STATEGY = "desktop"

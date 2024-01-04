from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, Type, Union


if TYPE_CHECKING:
    from .serializers import SVGChartSerializer

from dashboards.component import Component

@dataclass
class SVGChart(Component):
    template_name: str = "components/chart/svgchart.html"
    mark_safe: bool = False

    value: Optional[Union[Callable[..., Any], Type["SVGChartSerializer"]]] = None
    defer: Optional[Union[Callable[..., Any], Type["SVGChartSerializer"]]] = None

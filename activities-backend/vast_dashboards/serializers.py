from typing import Any, Dict, List, Optional, Type
from django.template.loader import render_to_string

from dashboards.component.chart.serializers import BaseChartSerializer, ModelDataMixin

class SVGChartSerializerMixin:
    template_name: str = "components/chart/svg.html"
    meta_layout_attrs = ["width", "height", "background_color"]

    _meta: Type[Any]

    class Meta:
        background_color: Optional[str] = None
        width = 400
        height = 200

    def get_data(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def to_svg(self, data: Any) -> str:
        raise NotImplementedError

    @classmethod
    def serialize(cls, **kwargs) -> str:
        self = cls()
        request = kwargs.get("request")
        df = self.get_data(**kwargs)
        fig = self.to_svg(df)
        return fig

    @classmethod
    def render(cls, template_id, **kwargs) -> str:
        self = cls()
        value = cls.serialize(**kwargs)
        context = {
            "template_id": template_id,
            "value": value,
        }
        return render_to_string(cls.template_name, context)

class SVGCodeChartSerializer(SVGChartSerializerMixin, BaseChartSerializer):
    class Meta(SVGChartSerializerMixin.Meta, BaseChartSerializer.Meta):
        pass

class SVGChartSerializer(ModelDataMixin, SVGCodeChartSerializer):
    class Meta(ModelDataMixin.Meta, SVGCodeChartSerializer.Meta):
        pass

    _meta: Type["SVGChartSerializer.Meta"]

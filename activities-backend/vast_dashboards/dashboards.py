from django import forms
from dashboards.dashboard import Dashboard, ModelDashboard
from dashboards.component import Text, Chart, Table, Form, BasicTable
from dashboards.component.table import TableSerializer, SerializedTable
from dashboards.component.layout import ComponentLayout, HTML, Card, Header, Div
from dashboards.forms import DashboardForm
from dashboards.registry import registry

from vast_dashboards.data import DashboardData

from activity_data.models import *

class VASTDashboardMixin:
    def get_context(self, **kwargs) -> dict:
        context = super().get_context(**kwargs)
        context.update({'segment': f'dashboards:vast_dashboards_{self.__class__.__name__.lower()}'})
        # print("VASTDashboard: get_context()", context)
        return context
    # class Media:
    #     js = ("dashboards/js/dashboard.js",
    #           "dashboards/vendor/js/plotly.min.js",
    #           "dashboards/vendor/js/datatables.min.js")
    #     css = {
    #         "all": ("dashboards/vendor/css/datatables.min.css",),
    #     }


class ActivitiesForm(DashboardForm):
    activities = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        choices=(
            ("all", "All"),
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
        )
    )
class ActivitySerializer(TableSerializer):
    class Meta:
        title = "Activities"
        columns = {
            "name": "Name",
        }
        order = ["-name"]
        model = Activity

class ActivitiesDashboard(VASTDashboardMixin, Dashboard):
    welcome = Text(value="VAST Activities")
    # activities_form = Form(form=ActivitiesForm,)
    # animals = Chart(defer=DashboardData.fetch_animals)
    activities_table = Table(value=ActivitySerializer, grid_css_classes="span-12")

    class Meta:
        name = "Activities"

# https://www.djangodashboards.com/
class ActivityDashboard(VASTDashboardMixin, ModelDashboard):
    name = Text(mark_safe=True, icon='<i class="fa-up"></i>', grid_css_classes="span-12")
    details = BasicTable(css_classes="table table-hover align-middle table-description", grid_css_classes="span-12")
    animals = Chart(defer=DashboardData.fetch_animals)

    class Meta:
        name = "Activity"
        model = Activity

    class Layout(Dashboard.Layout):
        components = ComponentLayout(
            Card(
                 Div("details",
                     css_classes={"wrapper":"table-responsive"}, grid_css_classes="span-12"),
                 #heading="\uf19c  Activity",
                 grid_css_classes="span-12"
            ),
            "animals",
            grid_css_classes="span-12"
        )

    def get_name_value(self, **kwargs):
        print("get_name", self.object, self.object.name, kwargs)

        ch_artifacts = []
        for a in self.object.ch_artifact.all():
            ch_artifacts.append(a.name)

        content = f"<h4><i class=\"fa-solid fa-building-columns\"></i> Activity: &quot;{self.object.name}&quot;</h4>"
        return content

    def get_details_value(self, **kwargs):
        data = [
            {
                "attribute": "<strong>Description</strong>:",
                "value":     self.object.description
            },
            {
                "attribute": "<strong>Age</strong>:",
                "value":     self.object.age
            },
            {
                "attribute": "<strong>VAST Annotated Cultural Heritage Artifacts</strong>:",
                "value":     ', '.join([a.name for a in self.object.ch_artifact.all()])
            },
            {
                "attribute": "<strong>Europeana Annotated Cultural Heritage Artifacts</strong>:",
                "value":     ', '.join([f'<a href="{a.europeana_uriref}" target="_blank">&quot;{a.name}&quot;</a>' for a in self.object.europeana_ch_artifact.all()])
            },
        ]
        return SerializedTable(
            columns={"attribute": "<i class=\"fa-solid fa-building-columns\"></i> Activity:",
                     "value": self.object.name},
            data=data,
            columns_datatables=[],
            order=[],
        )

registry.register(ActivitiesDashboard)
registry.register(ActivityDashboard)

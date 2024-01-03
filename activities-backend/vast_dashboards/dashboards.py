from django import forms
from dashboards.dashboard import Dashboard, ModelDashboard
from dashboards.component import Text, Chart, Table, Form
from dashboards.component.table import TableSerializer
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

class ActivityDashboard(VASTDashboardMixin, ModelDashboard):
    welcome = Text(value="Welcome to Django Dashboards!")
    animals = Chart(defer=DashboardData.fetch_animals)

    class Meta:
        name = "Activity"
        model = Activity

registry.register(ActivitiesDashboard)
registry.register(ActivityDashboard)

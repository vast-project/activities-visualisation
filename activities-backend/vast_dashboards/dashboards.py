from dashboards.dashboard import Dashboard
from dashboards.component import Text, Chart
from dashboards.registry import registry

from vast_dashboards.data import DashboardData

class VASTDashboard(Dashboard):
    def get_context(self, **kwargs) -> dict:
        context = super().get_context(**kwargs)
        context.update({'segment': f'dashboards:vast_dashboards_{self.__class__.__name__.lower()}'})
        # print("VASTDashboard: get_context()", context)
        return context

class FirstDashboard(VASTDashboard):
    welcome = Text(value="Welcome to Django Dashboards!")
    animals = Chart(defer=DashboardData.fetch_animals)

    class Meta:
        name = "First Dashboard"

registry.register(FirstDashboard)

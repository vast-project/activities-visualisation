from django.apps import AppConfig


class VastDashboardsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vast_dashboards'

    def ready(self):
        # for registry
        import vast_dashboards.dashboards  # type: ignore # noqa

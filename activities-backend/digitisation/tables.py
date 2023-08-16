import django_tables2 as tables
from activity_data.models import *
from django.urls import reverse

class HTMxTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id  = self._meta.model.__name__
        self.url = reverse('dashboard-table-model', kwargs={'model': self.id})

    class Meta:
        template_name = "tables/bootstrap_htmx.html"
        fields = ['name', 'created_by']

class ActivityHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Activity
        attrs = {"class": "table table-activity"}

class ActivityStepHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ActivityStep
        attrs = {"class": "table table-activitystep"}

class EventHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Event
        attrs = {"class": "table table-event"}

class VisitorGroupHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = VisitorGroup
        attrs = {"class": "table table-visitorgroup"}

class VisitorHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Visitor
        attrs = {"class": "table table-visitor"}

class ProductHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Product
        attrs = {"class": "table table-product"}

class ProductStatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = ProductStatement
        attrs = {"class": "table table-productstatement"}

class StatementHTMxTable(HTMxTable):
    class Meta(HTMxTable.Meta):
        model = Statement
        attrs = {"class": "table table-statement"}

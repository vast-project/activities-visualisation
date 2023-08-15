import django_tables2 as tables
from activity_data.models import *

class HTMxTable(tables.Table):
    class Meta:
        model = Product
        template_name = "tables/bootstrap_htmx.html"

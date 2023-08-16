import sys
from django import template
from digitisation.tables import *
from digitisation.filters import *
from activity_data.models import *

register = template.Library()

@register.inclusion_tag("tables/table_htmx.html", takes_context=True)
def dashboard_table(context, model, *args, **kwargs):
    request = context['request']
    class_model = getattr(sys.modules[__name__], model)
    class_fltr  = getattr(sys.modules[__name__], model + 'Filter')
    class_table = getattr(sys.modules[__name__], model + 'HTMxTable')
    fltr = class_fltr(request=request.GET, queryset=class_model.objects.all())
    template_context = {
        'filter': fltr,
        'table': class_table(fltr.qs),
        'filter_url': "index",
        'request': request,
    }
    #context.push(template_context)
    return template_context

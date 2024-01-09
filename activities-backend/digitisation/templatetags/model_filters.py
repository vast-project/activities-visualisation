##
## Register template custom filters...
##
from django import template
register = template.Library()

@register.filter
def get_repository_url(value):
    return value.get_repository_url()
@register.filter(name="get_repository_uri")
def get_repository_uri(value):
    return value.get_repository_uri()
@register.filter
def get_absolute_url(value):
    return value.get_absolute_url()
@register.filter
def get_dashboard_absolute_url(value):
    return value.get_dashboard_absolute_url()

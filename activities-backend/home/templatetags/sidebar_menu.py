from django import template
from home.models import SidebarMenuItem

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu.html')
def sidebar_menu():
    menu_items = SidebarMenuItem.objects.all()
    return {'sidebar_menu_items': menu_items}

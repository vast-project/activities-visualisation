from django import template
from home.models import SidebarMenuItem

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu.html')
def sidebar_menu():
    #menu_items = SidebarMenuItem.objects.all()
    menu_items = (
        {'title': 'Add Activity', 'url': 'activity-wizard'},
        {'title': 'Add Event',    'url': 'event-visitorgroup-wizard'},
        {'title': 'Add QR Code',  'url': 'visitorgroupqrcode-wizard'},
        {'title': 'Add Visitor',  'url': 'visitor-wizard'},
    )
    return {'sidebar_menu_items': menu_items}

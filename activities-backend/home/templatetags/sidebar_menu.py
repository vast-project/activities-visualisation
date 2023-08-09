from django import template
from home.models import SidebarMenuItem

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu.html')
def sidebar_menu():
    #menu_items = SidebarMenuItem.objects.all()
    menu_items = (
        {'title': '1. Add Activity',    'url': 'activity-wizard'},
        {'title': '2. Add Event',       'url': 'event-visitorgroup-wizard'},
        {'title': '3. Add QR Code',     'url': 'visitorgroupqrcode-wizard'},
        {'title': '4. Add Visitor',     'url': 'visitor-wizard'},
        {'title': '5. Add Product',     'url': 'product-wizard'},
        {'title': '6. Add Statements',  'url': 'statement-wizard'},
    )
    return {'sidebar_menu_items': menu_items}

from django import template
from home.models import SidebarMenuItem

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu.html')
def sidebar_menu(*args, **kwargs):
    #menu_items = SidebarMenuItem.objects.all()
    menu_items = (
        {'title': 'Add Activity',           'url': 'activity-wizard'},
        {'title': 'Add Event',              'url': 'event-visitorgroup-wizard'},
        {'title': 'Add QR Code',            'url': 'visitorgroupqrcode-wizard'},
        {'title': 'Add Visitor',            'url': 'visitor-wizard'},
        {'title': 'Add Product',            'url': 'product-wizard'},
        {'title': 'Add Statements',         'url': 'statement-wizard'},
        {'title': 'Add Product Statements', 'url': 'productstatement-wizard'},
       #{'title': 'Test Exceptions',        'url': 'exception-wizard'},
    )
    context = {'sidebar_menu_items': menu_items}
    for arg in args:
        context.update(arg)

    context.update(kwargs)
    return context

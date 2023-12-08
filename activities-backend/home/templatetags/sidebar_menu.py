from django import template
from django.urls import reverse
from home.models import SidebarMenuItem

register = template.Library()

@register.inclusion_tag('includes/sidebar_menu.html')
def sidebar_menu(*args, **kwargs):
    # print('sidebar_menu():', args, kwargs)
    category = kwargs.get('category', 'wizards')
    #menu_items = SidebarMenuItem.objects.all()
    match category:
        case 'dashboards':
            menu_items = (
                {'title': 'Activities',             'url': 'dashboards:vast_dashboards_activitiesdashboard'},
            )
        case _:
            menu_items = (
                {'title': 'Add Activity',           'url': 'activity-wizard'},
                {'title': 'Add Event',              'url': 'event-visitorgroup-wizard'},
                {'title': 'Add QR Code',            'url': 'qrcode-visitorgroup-wizard'},
                {'title': 'Import Visitors',        'url': 'import-questionnaire-visitors-wizard'},
                {'title': 'Add Visitor',            'url': 'visitor-wizard'},
                {'title': 'Add VirtualVisitor',     'url': 'virtualvisitor-wizard'},
                {'title': 'Add Product',            'url': 'product-wizard'},
                {'title': 'Add Statements',         'url': 'statement-wizard'},
                {'title': 'Add Product Statements', 'url': 'productstatement-wizard'},
               #{'title': 'Test Exceptions',        'url': 'exception-wizard'},
            )
    mi = []
    for item in menu_items:
        item['reverse_url'] = reverse(item['url'], kwargs=item.get('kwargs'))+'/' # Adding a slash to not having multiple menu items active
        mi.append(item)
    context = {'sidebar_menu_items': mi}
    for arg in args:
        context.update(arg)

    context.update(kwargs)
    return context

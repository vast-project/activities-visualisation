from django.urls import path, re_path

from .views import *

##
## Activity, Event, VisitorGroup Wizard
##

activity_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_activity', SelectActivityForm),
        ('add_activity', ActivityForm),
    ),
    condition_dict = {
        'add_activity':  lambda wizard: SelectActivityForm.addNew(wizard, 'ask_activity'),
    },
    extra_context = { 'segment': 'activity-wizard' },
    url_name='activity-wizard-step', done_step_name='finished'
)

event_visitorgroup_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_event',           SelectEventForm),
        ('add_event',           EventForm),
        ('ask_visitorgroup',    SelectVisitorGroupForm),
        ('add_visitorgroup',    VisitorGroupForm),
    ),
    condition_dict = {
        'add_event':            lambda wizard: SelectEventForm.addNew(wizard, 'ask_event'),
        'add_visitorgroup':     lambda wizard: SelectVisitorGroupForm.addNew(wizard, 'ask_visitorgroup'),
    },
    extra_context = { 'segment': 'event-visitorgroup-wizard' },
    url_name='event-visitorgroup-wizard-step', done_step_name='finished'
)

##
## QR Code Wizard
##
qrcode_wizard=ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_qrcode', SelectVisitorGroupQRCodeForm),
        ('add_qrcode', VisitorGroupQRCodeForm),
    ),
    condition_dict = {
        'add_qrcode':  lambda wizard: SelectVisitorGroupQRCodeForm.addNew(wizard, 'ask_qrcode'),
    },
    extra_context = { 'segment': 'visitorgroupqrcode-wizard' },
    url_name='visitorgroupqrcode-wizard-step', done_step_name='finished'
)

##
## Visitor Wizard
##
visitor_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_visitor', SelectVisitorForm),
        ('add_visitor', VisitorForm),
    ),
    condition_dict = {
        'add_visitor':  lambda wizard: SelectVisitorForm.addNew(wizard, 'ask_visitor'),
    },
    extra_context = { 'segment': 'visitor-wizard' },
    url_name='visitor-wizard-step', done_step_name='finished'
)

##
## Product Wizard
##
product_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_product', SelectProductForm),
        ('add_product', ProductForm),
    ),
    condition_dict = {
        'add_product':  lambda wizard: SelectProductForm.addNew(wizard, 'ask_product'),
    },
    extra_context = { 'segment': 'product-wizard' },
    url_name='product-wizard-step', done_step_name='finished'
)

##
## Statement Wizard
##
statement_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        #('ask_statement', SelectStatementForm),
        ('add_statement', ProductStatementsForm),
    ),
    condition_dict = {
        #'add_statement':  lambda wizard: SelectStatementForm.addNew(wizard, 'ask_statement'),
    },
    extra_context = { 'segment': 'statement-wizard' },
    url_name='statement-wizard-step', done_step_name='finished'
)

##
## ProductStatement Wizard
##
productstatement_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('add_productstatement', ProductProductStatementsForm),
    ),
    extra_context = { 'segment': 'productstatement-wizard' },
    url_name='productstatement-wizard-step', done_step_name='finished'
)

##
## Test Exception Wizard
##
exception_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_exception', SelectExceptionForm),
    ),
    extra_context = { 'segment': 'exception-wizard' },
    url_name='exception-wizard-step', done_step_name='finished'
)


##
## URLs
##
urlpatterns = [
    path('dashboard/table/<str:model>', ActivityHTMxTableView.as_view(), name='dashboard-table-model'),
    re_path(r'^wizard/activity/(?P<step>.+)/$', activity_wizard, name='activity-wizard-step'),
    path('wizard/activity', activity_wizard, name='activity-wizard'),
    re_path(r'^wizard/event-visitorgroup/(?P<step>.+)/$', event_visitorgroup_wizard, name='event-visitorgroup-wizard-step'),
    path('wizard/event-visitorgroup', event_visitorgroup_wizard, name='event-visitorgroup-wizard'),
    re_path(r'^wizard/visitorgroupqrcode/(?P<step>.+)/$', qrcode_wizard, name='visitorgroupqrcode-wizard-step'),
    path('wizard/visitorgroupqrcode', qrcode_wizard, name='visitorgroupqrcode-wizard'),
    re_path(r'^wizard/visitor/(?P<step>.+)/$', visitor_wizard, name='visitor-wizard-step'),
    path('wizard/visitor', visitor_wizard, name='visitor-wizard'),
    re_path(r'^wizard/product/(?P<step>.+)/$', product_wizard, name='product-wizard-step'),
    path('wizard/product', product_wizard, name='product-wizard'),
    re_path(r'^wizard/statement/(?P<step>.+)/$', statement_wizard, name='statement-wizard-step'),
    path('wizard/statement', statement_wizard, name='statement-wizard'),
    re_path(r'^wizard/productstatement/(?P<step>.+)/$', productstatement_wizard, name='productstatement-wizard-step'),
    path('wizard/productstatement', productstatement_wizard, name='productstatement-wizard'),
    #re_path(r'^wizard/exception/(?P<step>.+)/$', exception_wizard, name='exception-wizard-step'),
    #path('wizard/exception', exception_wizard, name='exception-wizard'),
]

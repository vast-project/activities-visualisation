from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

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
    extra_context = { 'segment': 'event-visitorgroup-wizard', 'save_on_steps': ('add_event',), },
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
    extra_context = { 'segment': 'qrcode-visitorgroup-wizard' },
    url_name='qrcode-visitorgroup-wizard-step', done_step_name='finished'
)

##
## Import Visitors from Questionnaires Wizard
##
import_questionnaire_visitors_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('select_activity_step',    ImportVisitorsSelectActivityStepForm),
        ('show_activity_step',      ImportVisitorsShowActivityStepForm),
    ),
    condition_dict = {
    },
    extra_context = { 'segment': 'import-questionnaire-visitors-wizard' },
    url_name='import-questionnaire-visitors-wizard-step', done_step_name='finished'
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
## VirtualVisitor Wizard
##
virtualvisitor_wizard = ActivityDigitisationWizardView.as_view(
    form_list = (
        ('ask_virtualvisitor', SelectVirtualVisitorForm),
        ('add_virtualvisitor', VirtualVisitorForm),
    ),
    condition_dict = {
        'add_virtualvisitor':  lambda wizard: SelectVirtualVisitorForm.addNew(wizard, 'ask_virtualvisitor'),
    },
    extra_context = { 'segment': 'virtualvisitor-wizard' },
    url_name='virtualvisitor-wizard-step', done_step_name='finished'
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
    path('dashboard/table/<str:model>',                     login_required(ActivityHTMxTableView.as_view()),       name='dashboard-table-model'),
    re_path(r'^wizard/activity/(?P<step>.+)/$',             login_required(activity_wizard),                       name='activity-wizard-step'),
    path('wizard/activity',                                 login_required(activity_wizard),                       name='activity-wizard'),
    re_path(r'^wizard/event-visitorgroup/(?P<step>.+)/$',   login_required(event_visitorgroup_wizard),             name='event-visitorgroup-wizard-step'),
    path('wizard/event-visitorgroup',                       login_required(event_visitorgroup_wizard),             name='event-visitorgroup-wizard'),
    re_path(r'^wizard/qrcode-visitorgroup/(?P<step>.+)/$',  login_required(qrcode_wizard),                         name='qrcode-visitorgroup-wizard-step'),
    path('wizard/qrcode-visitorgroup',                      login_required(qrcode_wizard),                         name='qrcode-visitorgroup-wizard'),
    re_path(r'^wizard/import-visitors/(?P<step>.+)/$',      login_required(import_questionnaire_visitors_wizard),  name='import-questionnaire-visitors-wizard-step'),
    path('wizard/import-visitors',                          login_required(import_questionnaire_visitors_wizard),  name='import-questionnaire-visitors-wizard'),
    re_path(r'^wizard/virtualvisitor/(?P<step>.+)/$',       login_required(virtualvisitor_wizard),                 name='virtualvisitor-wizard-step'),
    path('wizard/virtualvisitor',                           login_required(virtualvisitor_wizard),                 name='virtualvisitor-wizard'),
    re_path(r'^wizard/visitor/(?P<step>.+)/$',              login_required(visitor_wizard),                        name='visitor-wizard-step'),
    path('wizard/visitor',                                  login_required(visitor_wizard),                        name='visitor-wizard'),
    re_path(r'^wizard/product/(?P<step>.+)/$',              login_required(product_wizard),                        name='product-wizard-step'),
    path('wizard/product',                                  login_required(product_wizard),                        name='product-wizard'),
    re_path(r'^wizard/statement/(?P<step>.+)/$',            login_required(statement_wizard),                      name='statement-wizard-step'),
    path('wizard/statement',                                login_required(statement_wizard),                      name='statement-wizard'),
    re_path(r'^wizard/productstatement/(?P<step>.+)/$',     login_required(productstatement_wizard),               name='productstatement-wizard-step'),
    path('wizard/productstatement',                         login_required(productstatement_wizard),               name='productstatement-wizard'),
    #re_path(r'^wizard/exception/(?P<step>.+)/$',           login_required(exception_wizard),                      name='exception-wizard-step'),
    #path('wizard/exception',                               login_required(exception_wizard),                      name='exception-wizard'),
]

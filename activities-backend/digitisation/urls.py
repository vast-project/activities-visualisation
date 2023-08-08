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
## URLs
##
urlpatterns = [
    re_path(r'^wizard/activity/(?P<step>.+)/$', activity_wizard, name='activity-wizard-step'),
    path('wizard/activity', activity_wizard, name='activity-wizard'),
    re_path(r'^wizard/event-visitorgroup/(?P<step>.+)/$', event_visitorgroup_wizard, name='event-visitorgroup-wizard-step'),
    path('wizard/event-visitorgroup', event_visitorgroup_wizard, name='event-visitorgroup-wizard'),
    re_path(r'^wizard/visitorgroupqrcode/(?P<step>.+)/$', qrcode_wizard, name='visitorgroupqrcode-wizard-step'),
    path('wizard/visitorgroupqrcode', qrcode_wizard, name='visitorgroupqrcode-wizard'),
]

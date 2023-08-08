from django.urls import path, re_path

from .views import *

##
## Activity, Event, VisitorGroup Wizard
##
activity_event_visitorgroup_forms = (
    ('ask_activity',         SelectActivityForm),
    ('add_activity',         ActivityForm),
    ('ask_event',            SelectEventForm),
    ('add_event',            EventForm),
    ('ask_visitorgroup',     SelectVisitorGroupForm),
    ('add_visitorgroup',     VisitorGroupForm),
)
    #('add_activity_step', ActivityStepFormSet),
activity_event_visitorgroup_conditions = {
    'add_activity':      lambda wizard: SelectActivityForm.addNew(wizard, 'ask_activity'),
    'add_event':         lambda wizard: SelectEventForm.addNew(wizard, 'ask_event'),
    'add_visitorgroup':  lambda wizard: SelectVisitorGroupForm.addNew(wizard, 'ask_visitorgroup'),
}

activity_event_visitorgroup_wizard = ActivityDigitisationWizardView.as_view(
    form_list = activity_event_visitorgroup_forms,
    condition_dict = activity_event_visitorgroup_conditions,
    extra_context = { 'segment': 'activity-event-visitorgroup-wizard' },
    url_name='activity-event-visitorgroup-wizard-step', done_step_name='finished'
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
    re_path(r'^wizard/activity-event-visitorgroup/(?P<step>.+)/$', activity_event_visitorgroup_wizard, name='activity-event-visitorgroup-wizard-step'),
    path('wizard/activity-event-visitorgroup', activity_event_visitorgroup_wizard, name='activity-event-visitorgroup-wizard'),
    re_path(r'^wizard/visitorgroupqrcode/(?P<step>.+)/$', qrcode_wizard, name='visitorgroupqrcode-wizard-step'),
    path('wizard/visitorgroupqrcode', qrcode_wizard, name='visitorgroupqrcode-wizard'),
]

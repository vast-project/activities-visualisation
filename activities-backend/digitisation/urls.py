from django.urls import path, re_path

from .views import *

activity_digitisation_forms = (
    ('ask_activity',         SelectActivityForm),
    ('add_activity',         ActivityForm),
    ('ask_event',            SelectEventForm),
    ('add_event',            EventForm),
    ('ask_visitorgroup',     SelectVisitorGroupForm),
    ('add_visitorgroup',     VisitorGroupForm),
)
    #('add_activity_step', ActivityStepFormSet),
activity_digitisation_conditions = {
    'add_activity':      lambda wizard: SelectActivityForm.addNew(wizard, 'ask_activity'),
    'add_event':         lambda wizard: SelectEventForm.addNew(wizard, 'ask_event'),
    'add_visitorgroup':  lambda wizard: SelectVisitorGroupForm.addNew(wizard, 'ask_visitorgroup'),
}

activity_digitisation_wizard = ActivityDigitisationWizardView.as_view(
    form_list = activity_digitisation_forms,
    condition_dict = activity_digitisation_conditions,
    extra_context = { 'segment': 'activity-digitisation' },
    url_name='activity-digitisation-wizard-step', done_step_name='finished'
)

urlpatterns = [
    re_path(r'^wizard/activity-digitisation/(?P<step>.+)/$', activity_digitisation_wizard, name='activity-digitisation-wizard-step'),
    path('wizard/activity-digitisation', activity_digitisation_wizard, name='activity-digitisation-wizard'),
]

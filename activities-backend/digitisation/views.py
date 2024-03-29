from django.shortcuts import render
from formtools.wizard.views import SessionWizardView, NamedUrlSessionWizardView
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import sys

import logging
logger = logging.getLogger(__name__)

##
## Form Wizards
##
from .forms import *
from activity_data.admin import *
from activity_data.models import *

class ActivityDigitisationWizardView(LoginRequiredMixin, NamedUrlSessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, ''))
    template_name = "activity-digitisation-crispy.html"
    #template_name = "activity-digitisation.html"
    wizard_done_template = "pages/wizard-done.html"

    @property
    def saved_steps_instances(self):
        if 'saved_steps_instances' not in self.storage.data:
            self.storage.data['saved_steps_instances'] = {}
        return self.storage.data['saved_steps_instances']
    @saved_steps_instances.setter
    def saved_steps_instances(self, value):
        self.storage.data['saved_steps_instances'] = value

    # instances = {
    #     #'activity': Activity.objects.all().first(),
    # }

    # def get_form(self, step=None, data=None, files=None):
    #     mystep = step
    #     if step is None:
    #         mystep = self.steps.current
    #     form_class = self.get_form_list()[mystep]
    #     if hasattr(form_class, "AdminForm") and \
    #        hasattr(form_class.AdminForm, "admin_form_class"):
    #         admin_class = form_class.AdminForm.admin_form_class
    #         return admin_class(form_class._meta.model, admin.site).get_form(request=self.request)
    #     return super().get_form(step=step, data=data, files=files)

    def get_current_user(self):
        return self.request.user

    def get_form_initial(self, step):
        initial = self.initial_dict.get(step, {})
        initial.update({'created_by': self.get_current_user()})
        return initial

    def get_prefix(self, request, *args, **kwargs):
        prefix = super().get_prefix(request, *args, **kwargs)
        return prefix + self.url_name

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        kwargs.update({'wizard_view': self})
        return kwargs

    # def get_form_instance(self, step):
    #     instance = self.instance_dict.get(step, None)
    #     return instance
    #     # if instance == None:
    #     #     match self.steps.current:
    #     #         case 'add_activity_step':
    #     #             instance = self.instances.get('activity', None)
    #     # print("get_form_instance:", step, instance)
    #     # return instance

    # def get_form(self, step=None, data=None, files=None):
    #     d = super().get_form(step, data, files)
    #     if step is None:
    #         step = self.steps.current
    #     print("=====================================")
    #     print("GET FORM:", step, data)
    #     if step == 'add_activity':
    #         print(d)
    #     return d

    # def get_context_data(self, form, **kwargs):
    #     context = super().get_context_data(form=form, **kwargs)
    #     print("Context:", context)
    #     # match self.steps.current:
    #     #     case 'add_activity':
    #     #         form = ActivityStepFormSet()
    #     #         ## Form helper is not needed if we have provided a form...
    #     #         #form.helper = ActivityStepFormSetHelper(ActivityStepForm())
    #     #         context.update({
    #     #             'activity_steps': form,
    #     #         })
    #     # print("Context:", context)
    #     return context

    def process_step(self, form):
        # Get the form context
        context = self.get_context_data(form)
        # Is this step listed in context's save_on_steps?
        save_on_steps = context.get('save_on_steps')
        if save_on_steps and self.steps.current in save_on_steps:
            logger.info(f"process_step(): Saving on step: {self.steps.current}")
            # If this is a model form, save the data!
            if hasattr(form, 'save') and callable(form.save):
                logger.info(f"process_step(): Form can be saved: {form.instance}")
                saved_steps_instances = []
                # Create, but don't save the new model instance.
                instances = form.save(commit=False)
                user = self.get_current_user()
                if isinstance(instances, tuple):
                    # If result is a tuple, it is a model instance,
                    # that has a list of formsets.
                    instance = instances[0]
                else:
                    instance = instances
                # Save the main instance...
                instance.created_by = user
                instance.save()
                saved_steps_instances.append((instance.__class__.__name__, instance.pk))
                # Iterate over formsets, and save all instances...
                if isinstance(instances, tuple):
                    for formset in instances[1:]:
                        # The first tuple is the set of properties...
                        attrs = formset[0]
                        for inst in formset[1]:
                            inst.created_by = user
                            for attr in attrs:
                                setattr(inst, attr, instance)
                                inst.save()
                                saved_steps_instances.append((inst__class__.__name__, inst.pk))
                form.save_m2m()
                logger.info(f"process_step(): Form saved on step: {self.steps.current}")
                self.saved_steps_instances[self.steps.current] = saved_steps_instances
        return super().process_step(form)

    def get_form_instance(self, step):
        # Return the saved instance if has been saved before
        if step in self.saved_steps_instances:
            classname, pk = self.saved_steps_instances[step][0] # TODO: Fix embedded formsets
            cls = getattr(sys.modules[__name__], classname, None)
            if cls:
                try:
                    instance = cls.objects.get(pk=pk)
                except (KeyError, cls.DoesNotExist):
                    instance = super().get_form_instance(step)
            else:
                instance = super().get_form_instance(step)
        else:
            instance = super().get_form_instance(step)
        logger.info(f"get_form_instance({step}): {instance}")
        return instance

    def render_done(self, form, **kwargs):
        try:
            done_response = super().render_done(form, **kwargs)
            return done_response
        except Exception as e:
            form.add_error(None, e)
            return self.render(form)

    def done(self, form_list, form_dict, **kwargs):
        # for form_name in form_dict:
        #     print("Form:", form_name, form_dict[form_name].cleaned_data, form_dict[form_name].data)
        for form in form_list:
            if hasattr(form, 'save') and callable(form.save):
                form.save()
        return TemplateResponse(self.request, self.wizard_done_template, {
            'form_list': form_list,
            'form_dict': form_dict,
        })
        #return HttpResponseRedirect('/')

##
## Model Tables...
##
from django_tables2 import SingleTableMixin
from django_filters.views import FilterView
from .tables import *
from .filters import *
import sys
import json

class ActivityHTMxTableView(LoginRequiredMixin, SingleTableMixin, FilterView):
    table_class     = None
    queryset        = None
    filterset_class = None
    paginate_by     = 100

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        # print("ActivityHTMxTableView: setup():", args, kwargs, self.args, self.kwargs)
        class_name = self.kwargs.get('model', None)
        if class_name:
            class_model = getattr(sys.modules[__name__], class_name)
            self.queryset = class_model.objects.all().order_by('name')
            if not self.filterset_class:
                self.filterset_class = getattr(sys.modules[__name__],
                                               class_name + 'Filter')
            if not self.table_class:
                self.table_class     = getattr(sys.modules[__name__],
                                               class_name + 'HTMxTable')

    def get_template_names(self):
        # print("get_template_names()", self.args, self.kwargs)
        if self.request.htmx:
            template_name = "tables/table_partial.html"
        else:
            template_name = "tables/table_htmx.html"
        return template_name

    # def get_table_class(self):
    #     print("get_filterset_class():", self.args, self.kwargs)
    #     table_class = super().get_table_class()
    #     class_name = self.kwargs.get('model', None)
    #     if class_name and class_name != table_class.__name__:
    #         table_class = getattr(sys.modules[__name__],
    #                               class_name + 'HTMxTable')
    #     return table_class

    # def get_filterset_class(self):
    #     print("get_filterset_class():", self.args, self.kwargs)
    #     filterset_class = super().get_filterset_class()
    #     class_name = self.kwargs.get('model', None)
    #     if class_name and class_name != filterset_class.__name__:
    #         filterset_class = getattr(sys.modules[__name__],
    #                                   class_name + 'Filter')
    #     return filterset_class

    def get_table_kwargs(self):
        kwargs = super().get_table_kwargs()
        selected_rows = self.request.GET.getlist("selected", None)
        if selected_rows:
            selected_rows = [int(_) for _ in selected_rows]
            kwargs["selected_rows"] = selected_rows
        selection_data = self.request.GET.get("selection_data", None)
        if selection_data:
            selection_data = json.loads(selection_data)
            for key,value in selection_data.items():
                selection_data[key] = [int(_) for _ in value]
            kwargs['selection_data'] = selection_data
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context.update(kwargs)
        context.update(self.kwargs)
        # print('get_context_data():', context)
        return context

##
## Model Search Autocomplete...
##
from dal import autocomplete

class VASTModelAutocompleteView(autocomplete.Select2QuerySetView):

    def dispatch(self, request, *args, **kwargs):
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(args, kwargs)
        self.class_name = self.kwargs.get('model', 'Concept')
        self.class_model = getattr(sys.modules[__name__], self.class_name)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.class_model.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


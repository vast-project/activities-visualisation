from django import forms
from django.db.models import Q
import django_filters
from django.contrib.auth.models import User
from activity_data.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.utils.safestring import mark_safe
from django.urls import reverse
import json

class VASTObjectFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="",
        widget=forms.TextInput(attrs={
            "type": "search",
            "hx-trigger": "keyup changed delay:500ms, search",
            "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",
        })
    )

    filter_if_selected = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id  = self._meta.model.__name__
        # self.id  = self._meta.model._meta.model_name
        self.url = reverse('dashboard-table-model', kwargs={'model': self.id})
        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.layout = Layout(
          Row(
            Column(
              PrependedText('query',
                mark_safe('<i class="fas fa-search" aria-hidden="true"></i>'),
                placeholder="Type here...",
                hx_get=self.url,
                hx_indicator=f".progress-{self.id}",
                hx_target=f".table-container-{self.id}",
                id=f"id_query-{self.id}",
              ),
              css_class="col-lg-8 col-md-8 ms-3",
            ),
            Column(
              FormActions(
                Submit('submit', 'Search'),
              ),
              css_class="col-lg-2 col-md-2",
            ),
          )
        )
        # Get selection_data...
        selection_data = None
        if kwargs.get('data'):
            selection_data = kwargs['data'].get('selection_data')
        if selection_data:
            selection_data = json.loads(selection_data)
            for key,value in selection_data.items():
                selection_data[key] = [int(_) for _ in value]
        self.selection_data = selection_data
        # print(self.id, kwargs, flush=True)

    def universal_search(self, queryset, name, value):
        return self._meta.model.objects.filter(
            Q(name__icontains=value)
        )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        if user.is_superuser:
            result = parent
        else:
            group_users = {user, }
            for group in user.groups.all():
                group_users.update(User.objects.filter(groups__id=group.pk))
            # print("Users:", group_users)
            result = parent.filter(created_by__in=group_users)
        # print(result.model, parent.count(), result.count())
        # Check if we need to do additional filtering...
        if self.selection_data and self.filter_if_selected:
            for key,value in self.filter_if_selected.items():
                if key in self.selection_data:
                    pks = self.selection_data[key]
                    if len(pks):
                        # print(result.model, value, pks, result.count())
                        result = result.filter(**{value: pks}).distinct()
                        # print("===>", result.count())
        return result.distinct()

    class Meta:
        model = VASTObject
        fields = ['query']

class ActivityFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Activity

class ActivityStepFilter(VASTObjectFilter):
    filter_if_selected = {
        'Activity': 'activity__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = ActivityStep

class EventFilter(VASTObjectFilter):
    filter_if_selected = {
        'Activity': 'activity__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = Event

class VisitorGroupFilter(VASTObjectFilter):
    filter_if_selected = {
        'Event': 'event__in',
        'Activity': 'event__activity__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = VisitorGroup

class VisitorFilter(VASTObjectFilter):
    filter_if_selected = {
        'Activity': 'activity__in',
        'VisitorGroup': 'visitor_group__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = Visitor

class VirtualVisitorFilter(VASTObjectFilter):
    filter_if_selected = {
        'Activity': 'activity__in',
        'VisitorGroup': 'visitor_group__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = VirtualVisitor

class ProductFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'visitor__in',
        'ActivityStep': 'activity_step__in',
        'Activity': 'visitor__activity__in',
        'VisitorGroup': 'visitor__visitor_group__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = Product

class ProductStatementFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'subject__visitor__in',
        'ActivityStep': 'subject__activity_step__in',
        'Activity': 'subject__visitor__activity__in',
        'VisitorGroup': 'subject__visitor__visitor_group__in',
        'Product': 'subject__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = ProductStatement

class StatementFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'product__visitor__in',
        'ActivityStep': 'product__activity_step__in',
        'Activity': 'product__visitor__activity__in',
        'VisitorGroup': 'product__visitor__visitor_group__in',
        'Product': 'product__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = Statement

class QuestionnaireEntryFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'product__visitor__in',
        'ActivityStep': 'product__activity_step__in',
        'Activity': 'product__visitor__activity__in',
        'VisitorGroup': 'product__visitor__visitor_group__in',
        'Product': 'product__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = QuestionnaireEntry

class QuestionnaireQuestionFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'questionnaireanswer__questionnaire_entry__product__visitor__in',
        'ActivityStep': 'questionnaireanswer__questionnaire_entry__product__activity_step__in',
        'Activity': 'questionnaireanswer__questionnaire_entry__product__visitor__activity__in',
        'VisitorGroup': 'questionnaireanswer__questionnaire_entry__product__visitor__visitor_group__in',
        'Product': 'questionnaireanswer__questionnaire_entry__product__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = QuestionnaireQuestion

class QuestionnaireAnswerFilter(VASTObjectFilter):
    filter_if_selected = {
        'Visitor': 'questionnaire_entry__product__visitor__in',
        'ActivityStep': 'questionnaire_entry__product__activity_step__in',
        'Activity': 'questionnaire_entry__product__visitor__activity__in',
        'VisitorGroup': 'questionnaire_entry__product__visitor__visitor_group__in',
        'Product': 'questionnaire_entry__product__in',
        'QuestionnaireEntry': 'questionnaire_entry__in',
        'QuestionnaireQuestion': 'question__in',
    }
    class Meta(VASTObjectFilter.Meta):
        model = QuestionnaireAnswer

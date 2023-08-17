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

class VASTObjectFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search', label="",
        widget=forms.TextInput(attrs={
            "type": "search",
            "hx-trigger": "keyup changed delay:500ms, search",
            "x-on:htmx:before-request": "$dispatch('clear-pagination-and-sort')",
        })
    )

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

    def universal_search(self, queryset, name, value):
        return self._meta.model.objects.filter(
            Q(name__icontains=value)
        )

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        if user.is_superuser:
            return parent
        group_users = {user, }
        for group in user.groups.all():
            group_users.update(User.objects.filter(groups__id=group.pk))
        # print("Users:", group_users)
        return parent.filter(created_by__in=group_users)

    class Meta:
        model = VASTObject
        fields = ['query']

class ActivityFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Activity

class ActivityStepFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = ActivityStep

class EventFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Event

class VisitorGroupFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = VisitorGroup

class VisitorFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Visitor

class ProductFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Product

class ProductStatementFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = ProductStatement

class StatementFilter(VASTObjectFilter):
    class Meta(VASTObjectFilter.Meta):
        model = Statement

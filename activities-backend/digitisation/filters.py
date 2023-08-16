from django.db.models import Q
import django_filters
from activity_data.models import *

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from django.utils.safestring import mark_safe

class VASTObjectFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.layout = Layout(
          Row(
            Column(
              PrependedText('query',
                mark_safe('<i class="fas fa-search" aria-hidden="true"></i>'),
                placeholder="Type here...",
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

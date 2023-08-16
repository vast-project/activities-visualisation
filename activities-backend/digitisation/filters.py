from django.db.models import Q
import django_filters
from activity_data.models import *

class VASTObjectFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='universal_search',
                                      label="")

    class Meta:
        model = VASTObject
        fields = ['query']

    def universal_search(self, queryset, name, value):
        return self._meta.model.objects.filter(
            Q(name__icontains=value)
        )

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

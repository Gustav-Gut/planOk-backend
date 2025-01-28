import django_filters
from ..models.models import Project

class ProjectFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    started_at = django_filters.DateFromToRangeFilter(field_name='started_at')

    class Meta:
        model = Project
        fields = ['address', 'status', 'name', 'started_at']
import django_filters
from ..models.models import Project, Unit

class ProjectFilter(django_filters.FilterSet):
    address = django_filters.CharFilter(field_name='address', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    started_at = django_filters.DateFromToRangeFilter(field_name='started_at')

    class Meta:
        model = Project
        fields = ['address', 'status', 'name', 'started_at']

class UnitFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='unit_status', lookup_expr='iexact')
    type = django_filters.CharFilter(field_name='unit_type', lookup_expr='iexact')
    project = django_filters.UUIDFilter(field_name='project', lookup_expr='exact')
    ordering = django_filters.OrderingFilter(fields=(('created_at', 'created_at'), ('price', 'price')))

    class Meta:
        model = Unit
        fields = ['unit_status', 'unit_type', 'project']
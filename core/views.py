from rest_framework import viewsets, filters
from .models import Project, Unit, Customer
from .serializers import (
    ProjectSerializer,
    UnitSerializer,
    CustomerSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'status']  # Búsqueda
    ordering_fields = ['created_at', 'name', 'started_at', 'finished_at']
    ordering = ['-created_at']


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('-created_at')
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['unit_number', 'unit_status', 'unit_type', 'reservation_deposit']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['rut', 'name', 'lastname', 'email', 'phone']
    ordering_fields = ['created_at', 'name', 'lastname']
    ordering = ['-created_at']

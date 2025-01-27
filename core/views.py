from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Unit, Customer
from .serializers import (
    ProjectSerializer,
    UnitSerializer,
    CustomerSerializer
)



class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['name', 'address', 'status']  # Búsqueda
    ordering_fields = ['created_at', 'started_at', 'finished_at']
    ordering = ['-created_at']


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('-created_at')
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['unit_status', 'unit_type', 'project']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        data = request.data
        
        # Si es una lista, asumimos creación múltiple
        if isinstance(data, list):
            serializer = self.get_serializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Si es un dict, usamos la creación por defecto de un solo objeto
        return super().create(request, *args, **kwargs)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rut', 'name', 'lastname', 'email', 'phone']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

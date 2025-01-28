from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from ..services.project_service import ProjectService
from ..services.unit_service import UnitService
from ..services.customer_service import CustomerService
from ..models.models import Unit, Customer
from ..serializers.serializers import (
    ProjectSerializer,
    UnitSerializer,
    CustomerSerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .filters import ProjectFilter

@extend_schema_view(
    list=extend_schema(
        summary="Listar proyectos",
        description="Retorna la lista de proyectos, con posibilidad de filtrar y ordenar.",
        parameters=[
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por nombre del proyecto.'
            ),
            OpenApiParameter(
                name='address',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por dirección (búsqueda parcial).'
            ),
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por estado (`Off Plan`, `Under Construction`, `Finished`, `Sold`, etc.).'
            ),
            OpenApiParameter(
                name='started_at__gte',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar por proyectos que empezaron después o en esta fecha (>=).'
            ),
            OpenApiParameter(
                name='started_at__lte',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar por proyectos que empezaron antes o en esta fecha (<=).'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Ordenar por `created_at`, `started_at`, `finished_at` (asc o desc). Ejemplo: `?ordering=-created_at`.'
            )
        ],
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value=[
                    {
                        "id": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                        "name": "Nuevo Proyecto",
                        "address": "Av. Ejemplo 123",
                        "description": "Descripción opcional del proyecto.",
                        "status": "Off Plan",
                        "started_at": "2025-01-01",
                        "finished_at": None,
                        "created_at": "2023-10-01T12:00:00Z"
                    }
                ],
                response_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Obtener un proyecto",
        description="Retorna los detalles de un proyecto específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "name": "Nuevo Proyecto",
                    "address": "Av. Ejemplo 123",
                    "description": "Descripción opcional del proyecto.",
                    "status": "Off Plan",
                    "started_at": "2025-01-01",
                    "finished_at": None,
                    "created_at": "2023-10-01T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Crear un proyecto",
        description="Crea un nuevo proyecto.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "name": "Nuevo Proyecto",
                    "address": "Av. Ejemplo 123",
                    "started_at": "2025-01-01",
                    "description": "Descripción opcional del proyecto.",
                    "status": "Off Plan"
                },
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "name": "Nuevo Proyecto",
                    "address": "Av. Ejemplo 123",
                    "description": "Descripción opcional del proyecto.",
                    "status": "Off Plan",
                    "started_at": "2025-01-01",
                    "finished_at": None,
                    "created_at": "2023-10-01T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    update=extend_schema(
        summary="Actualizar un proyecto",
        description="Actualiza todos los campos de un proyecto específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "name": "Proyecto Actualizado",
                    "address": "Av. Nueva Dirección 456",
                    "started_at": "2025-01-01",
                    "description": "Nueva descripción del proyecto.",
                    "status": "Under Construction"
                },
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "name": "Proyecto Actualizado",
                    "address": "Av. Nueva Dirección 456",
                    "description": "Nueva descripción del proyecto.",
                    "status": "Under Construction",
                    "started_at": "2025-01-01",
                    "finished_at": None,
                    "created_at": "2023-10-01T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un proyecto",
        description="Permite actualizar parcialmente un proyecto usando `PATCH`.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "status": "Finished",
                    "finished_at": "2025-12-31"
                },
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "name": "Nuevo Proyecto",
                    "address": "Av. Ejemplo 123",
                    "description": "Descripción opcional del proyecto.",
                    "status": "Finished",
                    "started_at": "2025-01-01",
                    "finished_at": "2025-12-31",
                    "created_at": "2023-10-01T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary="Eliminar un proyecto",
        description="Elimina un proyecto específico basado en su ID."
    )
)
class ProjectViewSet(viewsets.ModelViewSet):

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['created_at', 'started_at', 'finished_at']
    ordering = ['-created_at']

    def list(self, request):
        queryset = ProjectService.get_projects()
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ProjectSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = ProjectService.get_project_by_id(pk)
        if not project:
            return Response({"detail": "Proyecto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request):
        project = ProjectService.create_project(request.data)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = ProjectService.update_project(pk, request.data)
        if not project:
            return Response({"detail": "Proyecto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        project = ProjectService.partial_update_project(pk, request.data)
        if not project:
            return Response({"detail": "Proyecto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        deleted = ProjectService.delete_project(pk)
        if not deleted:
            return Response({"detail": "Proyecto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

@extend_schema_view(
    list=extend_schema(
        summary="Listar unidades",
        description="Retorna la lista paginada de unidades ordenadas por `-created_at`.",
        parameters=[
            OpenApiParameter(
                name='unit_status',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por estado de la unidad (`Available`, `Sold`, `Reserved`).'
            ),
            OpenApiParameter(
                name='unit_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por tipo de unidad (`Apartment`, `House`, etc.).'
            ),
            OpenApiParameter(
                name='project',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description='Filtrar por el ID del proyecto al que pertenece la unidad.'
            ),
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Ordenar por `created_at` (asc o desc) o `price` (asc o desc). Ejemplo: `?ordering=-price`.'
            )
        ],
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value=[
                    {
                        "id": "a1b2c3d4-5678-9101-1121-314151617181",
                        "unit_number": 1,
                        "unit_type": "Apartment",
                        "square_meters": 50.5,
                        "price": 150000000,
                        "status": "Available",
                        "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                        "created_at": "2025-01-27T12:00:00Z"
                    }
                ],
                response_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente una unidad",
        description="Permite actualizar parcialmente una unidad usando `PATCH`.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "status": "Reserved"
                },
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "a1b2c3d4-5678-9101-1121-314151617181",
                    "unit_number": 1,
                    "unit_type": "Apartment",
                    "square_meters": 50.5,
                    "price": 150000000,
                    "status": "Reserved",
                    "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "created_at": "2025-01-27T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    update=extend_schema(
        summary="Actualizar una unidad",
        description="Actualiza todos los campos de una unidad específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "id": "a1b2c3d4-5678-9101-1121-314151617181",
                    "unit_number": 1,
                    "unit_type": "Apartment",
                    "square_meters": 50.5,
                    "price": 150000000,
                    "status": "Reserved",
                    "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "created_at": "2025-01-27T12:00:00Z"
                },
                request_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Crear una o varias unidades",
        description="Crea una nueva unidad o varias unidades en una sola petición.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud (una unidad)',
                value={
                    "unit_number": 1,
                    "unit_type": "Apartment",
                    "square_meters": 50.5,
                    "price": 150000000,
                    "status": "Available",
                    "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194"
                },
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de solicitud (varias unidades)',
                value=[
                    {
                        "unit_number": 1,
                        "unit_type": "Apartment",
                        "square_meters": 50.5,
                        "price": 150000000,
                        "status": "Available",
                        "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194"
                    },
                    {
                        "unit_number": 2,
                        "unit_type": "House",
                        "square_meters": 120.0,
                        "price": 300000000,
                        "status": "Reserved",
                        "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194"
                    }
                ],
                request_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta (una unidad)',
                value={
                    "id": "a1b2c3d4-5678-9101-1121-314151617181",
                    "unit_number": 1,
                    "unit_type": "Apartment",
                    "square_meters": 50.5,
                    "price": 150000000,
                    "status": "Available",
                    "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "created_at": "2025-01-27T12:00:00Z"
                },
                response_only=True
            ),
            OpenApiExample(
                'Ejemplo de respuesta (varias unidades)',
                value=[
                    {
                        "id": "a1b2c3d4-5678-9101-1121-314151617181",
                        "unit_number": 1,
                        "unit_type": "Apartment",
                        "square_meters": 50.5,
                        "price": 150000000,
                        "status": "Available",
                        "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                        "created_at": "2025-01-27T12:00:00Z"
                    },
                    {
                        "id": "b2c3d4e5-6789-1011-2131-415161718192",
                        "unit_number": 2,
                        "unit_type": "House",
                        "square_meters": 120.0,
                        "price": 300000000,
                        "status": "Reserved",
                        "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                        "created_at": "2025-01-27T12:00:00Z"
                    }
                ],
                response_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary="Eliminar una unidad",
        description="Elimina una unidad específico basado en su ID."
    ),
    retrieve=extend_schema(
        summary="Obtener una unidad",
        description="Retorna los detalles de una unidad específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "a1b2c3d4-5678-9101-1121-314151617181",
                    "unit_number": 1,
                    "unit_type": "Apartment",
                    "square_meters": 50.5,
                    "price": 150000000,
                    "status": "Reserved",
                    "project": "f2f5a566-5619-43f9-8d3f-cf106e90e194",
                    "created_at": "2025-01-27T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
)
class UnitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['unit_status', 'unit_type', 'project']
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(UnitService.get_all_units())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UnitSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UnitSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            unit = UnitService.get_unit_by_id(pk)
            serializer = UnitSerializer(unit)
            return Response(serializer.data)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        data = request.data
        if isinstance(data, list):
            created_units = UnitService.create_multiple_units(data)
            serializer = UnitSerializer(created_units, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            unit = UnitService.create_unit(data)
            serializer = UnitSerializer(unit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            unit = UnitService.get_unit_by_id(pk)
            serializer = UnitSerializer(unit, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_unit = UnitService.update_unit(unit, serializer.validated_data)
            serializer = UnitSerializer(updated_unit)
            return Response(serializer.data)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None, *args, **kwargs):
        try:
            unit = UnitService.get_unit_by_id(pk)
            serializer = UnitSerializer(unit, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_unit = UnitService.update_unit(unit, serializer.validated_data)
            serializer = UnitSerializer(updated_unit)
            return Response(serializer.data)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            unit = UnitService.get_unit_by_id(pk)
            UnitService.delete_unit(unit)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Unit.DoesNotExist:
            return Response({'error': 'Unit not found'}, status=status.HTTP_404_NOT_FOUND)


@extend_schema_view(
    list=extend_schema(
        summary="Listar clientes",
        description="Retorna la lista de clientes ordenados por -created_at. Puedes filtrar por RUT, nombre, apellido, email o teléfono.",
        parameters=[
            OpenApiParameter(
                name='rut',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por RUT del cliente'
            ),
            OpenApiParameter(
                name='name',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por nombre del cliente'
            ),
            OpenApiParameter(
                name='lastname',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por apellido del cliente'
            ),
            OpenApiParameter(
                name='email',
                type=OpenApiTypes.EMAIL,
                location=OpenApiParameter.QUERY,
                description='Filtrar por correo electrónico del cliente'
            ),
            OpenApiParameter(
                name='phone',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por teléfono del cliente'
            ),
        ],
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value=[
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "rut": "12345678-9",
                        "name": "Juan",
                        "lastname": "Pérez",
                        "email": "juan.perez@example.com",
                        "phone": "+56912345678",
                        "created_at": "2023-10-01T12:00:00Z"
                    }
                ],
                response_only=True
            )
        ]
    ),
    retrieve=extend_schema(
        summary="Obtener un cliente",
        description="Retorna los detalles de un cliente específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de respuesta',
                value={
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "rut": "12345678-9",
                    "name": "Juan",
                    "lastname": "Pérez",
                    "email": "juan.perez@example.com",
                    "phone": "+56912345678",
                    "created_at": "2023-10-01T12:00:00Z"
                },
                response_only=True
            )
        ]
    ),
    create=extend_schema(
        summary="Crear un cliente",
        description="Crea un nuevo cliente con los datos proporcionados.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "rut": "12345678-9",
                    "name": "Juan",
                    "lastname": "Pérez",
                    "email": "juan.perez@example.com",
                    "phone": "+56912345678"
                },
                request_only=True
            )
        ]
    ),
    update=extend_schema(
        summary="Actualizar un cliente",
        description="Actualiza todos los campos de un cliente específico basado en su ID.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "rut": "12345678-9",
                    "name": "Juan",
                    "lastname": "Pérez",
                    "email": "juan.perez@example.com",
                    "phone": "+56912345678"
                },
                request_only=True
            )
        ]
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente un cliente",
        description="Permite actualizar parcialmente un cliente (PATCH). Solo se necesitan enviar los campos que se desean modificar.",
        examples=[
            OpenApiExample(
                'Ejemplo de solicitud',
                value={
                    "phone": "+56987654321"
                },
                request_only=True
            )
        ]
    ),
    destroy=extend_schema(
        summary="Eliminar un cliente",
        description="Elimina un cliente específico basado en su ID."
    )
)
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rut', 'name', 'lastname', 'email', 'phone']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    # Si quieres seguir usando el QuerySet para list/retrieve automáticos, mantenlo
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        customer = CustomerService.create_customer(request.data)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        try:
            customer = CustomerService.get_customer_by_id(kwargs['pk'])
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        updated_customer = CustomerService.update_customer(customer, request.data, partial=False)
        serializer = CustomerSerializer(updated_customer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        try:
            customer = CustomerService.get_customer_by_id(kwargs['pk'])
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        updated_customer = CustomerService.update_customer(customer, request.data, partial=True)
        serializer = CustomerSerializer(updated_customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            customer = CustomerService.get_customer_by_id(kwargs['pk'])
        except Customer.DoesNotExist:
            return Response({"detail": "Cliente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        CustomerService.delete_customer(customer)
        return Response(status=status.HTTP_204_NO_CONTENT)

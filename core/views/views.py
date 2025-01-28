from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from ..models.models import Project, Unit, Customer
from ..serializers import (
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
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ProjectFilter
    ordering_fields = ['created_at', 'started_at', 'finished_at']
    ordering = ['-created_at']

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
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['rut', 'name', 'lastname', 'email', 'phone']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

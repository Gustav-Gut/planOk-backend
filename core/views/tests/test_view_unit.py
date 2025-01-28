from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from core.models.models import Unit, Project
import json

class UnitViewSetTest(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_url = reverse('token_obtain_pair')
        token_response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        self.token = token_response.data['access']
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        # Crear un proyecto de prueba
        self.project = Project.objects.create(
            name="Proyecto Prueba",
            address="Av. Ejemplo 123",
            started_at="2025-01-01",
            status="Off Plan"
        )

        # Crear unidades de prueba
        self.unit = Unit.objects.create(
            unit_number="1",
            unit_type="Apartment",
            square_meters=50.5,
            price=150000000,
            unit_status="Available",
            project=self.project
        )

        self.list_url = reverse('units-list')  # URL para la lista de unidades
        self.detail_url = reverse('units-detail', args=[self.unit.id])  # URL para una unidad específica

    def test_list_units(self):
        """Prueba que se puedan listar las unidades"""
        response = self.client.get(self.list_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Solo una unidad debería estar presente
        self.assertEqual(response.data['results'][0]['unit_number'], "1")

    def test_retrieve_unit(self):
        """Prueba que se puedan obtener los detalles de una unidad"""
        response = self.client.get(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.unit.id))
        self.assertEqual(response.data['unit_number'], "1")

    def test_create_unit(self):
        """Prueba que se pueda crear una unidad"""
        data = {
            "unit_number": "2A",
            "unit_type": "House",
            "square_meters": 120.0,
            "price": 300000000,
            "status": "Available",
            "project": str(self.project.id)
        }
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )

        # Verifica la respuesta y el contenido creado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 2)
        self.assertEqual(Unit.objects.order_by('-created_at').first().unit_number, "2A")

    def test_create_multiple_units(self):
        """Prueba que se puedan crear varias unidades en una sola solicitud"""
        data = [
            {
                "unit_number": "2",
                "unit_type": "House",
                "square_meters": 120.0,
                "price": 300000000,
                "status": "Available",
                "project": str(self.project.id)
            },
            {
                "unit_number": "3",
                "unit_type": "Apartment",
                "square_meters": 80.0,
                "price": 200000000,
                "status": "Reserved",
                "project": str(self.project.id)
            }
        ]
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )

        # Verifica la respuesta y el contenido creado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Unit.objects.count(), 3)  # Ya había una unidad en setUp, ahora hay 3
        created_units = Unit.objects.order_by('-created_at')[:2]
        self.assertEqual(created_units[0].unit_number, "3")  # Última unidad creada
        self.assertEqual(created_units[1].unit_number, "2")  # Penúltima unidad creada

    def test_update_unit(self):
        """Prueba que se pueda actualizar completamente una unidad"""
        data = {
            "unit_number": 1,
            "unit_type": "Apartment",
            "square_meters": 60.0,
            "price": 200000000,
            "unit_status": "Reserved",
            "project": str(self.project.id)
        }
        response = self.client.put(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.square_meters, 60.0)
        self.assertEqual(self.unit.unit_status, "Reserved")

    def test_partial_update_unit(self):
        """Prueba que se pueda actualizar parcialmente una unidad"""
        data = {
            "unit_status": "Reserved"
        }
        response = self.client.patch(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.unit.refresh_from_db()
        self.assertEqual(self.unit.unit_status, "Reserved")

    def test_delete_unit(self):
        """Prueba que se pueda eliminar una unidad"""
        response = self.client.delete(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Unit.objects.count(), 0)

    def test_filter_units_by_status(self):
        """Prueba que se puedan filtrar unidades por estado"""
        response = self.client.get(
            self.list_url,
            {'unit_status': 'Available'},
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['unit_status'], "Available")

    def test_order_units_by_price(self):
        """Prueba que se puedan ordenar las unidades por precio"""
        # Crear una segunda unidad
        Unit.objects.create(
            unit_number=2,
            unit_type="House",
            square_meters=120.0,
            price=300000000,
            unit_status="Available",
            project=self.project
        )
        response = self.client.get(self.list_url, {'ordering': '-price'}, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['price'], 300000000)

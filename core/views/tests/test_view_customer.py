from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from core.models.models import Customer
import json


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_url = reverse('token_obtain_pair')
        token_response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        self.token = token_response.data['access']
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        # Crear clientes de prueba
        self.customer = Customer.objects.create(
            rut="123456789",
            name="Juan",
            lastname="Pérez",
            email="juan.perez@example.com",
            phone="+56912345678"
        )

        self.list_url = reverse('customers-list')  # URL para la lista de clientes
        self.detail_url = reverse('customers-detail', args=[self.customer.id])  # URL para un cliente específico

    def test_list_customers(self):
        """Prueba que se puedan listar los clientes"""
        response = self.client.get(self.list_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Solo un cliente debería estar presente
        self.assertEqual(response.data['results'][0]['rut'], "123456789")

    def test_retrieve_customer(self):
        """Prueba que se puedan obtener los detalles de un cliente"""
        response = self.client.get(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.customer.id))
        self.assertEqual(response.data['name'], "Juan")

    def test_create_customer(self):
        """Prueba que se pueda crear un cliente"""
        data = {
            "rut": "987654321",
            "name": "Pedro",
            "lastname": "Gómez",
            "email": "pedro.gomez@example.com",
            "phone": "+56987654321"
        }
        response = self.client.post(
            self.list_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )

        # Verifica la respuesta y el contenido creado
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.order_by('-created_at').first().rut, "987654321")

    def test_update_customer(self):
        """Prueba que se pueda actualizar completamente un cliente"""
        data = {
            "rut": "123456789",
            "name": "Juan Actualizado",
            "lastname": "Pérez Actualizado",
            "email": "juan.actualizado@example.com",
            "phone": "+56911111111"
        }
        response = self.client.put(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "Juan Actualizado")
        self.assertEqual(self.customer.email, "juan.actualizado@example.com")

    def test_partial_update_customer(self):
        """Prueba que se pueda actualizar parcialmente un cliente"""
        data = {
            "phone": "+56999999999"
        }
        response = self.client.patch(
            self.detail_url,
            data=json.dumps(data),
            content_type='application/json',
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, "+56999999999")

    def test_delete_customer(self):
        """Prueba que se pueda eliminar un cliente"""
        response = self.client.delete(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_filter_customers_by_rut(self):
        """Prueba que se puedan filtrar clientes por RUT"""
        response = self.client.get(
            self.list_url,
            {'rut': '123456789'},
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['rut'], "123456789")

    def test_filter_customers_by_name(self):
        """Prueba que se puedan filtrar clientes por nombre"""
        response = self.client.get(
            self.list_url,
            {'name': 'Juan'},
            **self.auth_headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], "Juan")

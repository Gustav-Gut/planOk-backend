from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from core.models.models import Project


class ProjectViewSetTest(APITestCase):
    def setUp(self):
         # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token_url = reverse('token_obtain_pair')
        self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        token_response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpassword'})
        self.token = token_response.data['access']
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        # Crear datos iniciales para las pruebas
        self.project = Project.objects.create(
            name="Proyecto Prueba",
            address="Av. Ejemplo 123",
            started_at="2025-01-01",
            status="Off Plan"
        )
        self.list_url = reverse('projects-list')  # URL para la lista de proyectos
        self.detail_url = reverse('projects-detail', args=[self.project.id])  # URL para un proyecto específico


    def test_list_projects(self):
        """Prueba que se puedan listar los proyectos"""
        response = self.client.get(self.list_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Proyecto Prueba")

    def test_retrieve_project(self):
        """Prueba que se puedan obtener los detalles de un proyecto"""
        response = self.client.get(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.project.id))
        self.assertEqual(response.data['name'], "Proyecto Prueba")

    def test_create_project(self):
        """Prueba que se pueda crear un proyecto"""
        data = {
            "name": "Nuevo Proyecto",
            "address": "Av. Nueva Dirección 456",
            "started_at": "2025-02-01",
            "description": "Descripción opcional",
            "status": "Under Construction"
        }
        response = self.client.post(self.list_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        latest_project = Project.objects.order_by('-created_at').first()
        self.assertEqual(latest_project.name, "Nuevo Proyecto")

    def test_update_project(self):
        """Prueba que se pueda actualizar completamente un proyecto"""
        data = {
            "name": "Proyecto Actualizado",
            "address": "Av. Nueva Dirección 456",
            "started_at": "2025-01-01",
            "description": "Descripción actualizada",
            "status": "Finished",
            "finished_at": "2025-12-31"
        }
        response = self.client.put(self.detail_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Proyecto Actualizado")
        self.assertEqual(self.project.status, "Finished")
        self.assertEqual(self.project.finished_at.isoformat(), "2025-12-31")

    def test_partial_update_project(self):
        """Prueba que se pueda actualizar parcialmente un proyecto"""
        data = {
            "status": "Finished",
            "finished_at": "2025-12-31"
        }
        response = self.client.patch(self.detail_url, data, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "Finished")
        self.assertEqual(self.project.finished_at.isoformat(), "2025-12-31")

    def test_delete_project(self):
        """Prueba que se pueda eliminar un proyecto"""
        response = self.client.delete(self.detail_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)  # El proyecto debería haber sido eliminado

    def test_filter_projects_by_name(self):
        """Prueba que se puedan filtrar proyectos por nombre"""
        response = self.client.get(self.list_url, {'name': 'Proyecto Prueba'},  **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Proyecto Prueba")

    def test_filter_projects_by_status(self):
        """Prueba que se puedan filtrar proyectos por estado"""
        response = self.client.get(self.list_url, {'status': 'Off Plan'},  **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], "Off Plan")

    def test_order_projects_by_created_at(self):
        """Prueba que se puedan ordenar los proyectos por fecha de creación"""
        # Crear un segundo proyecto para verificar la ordenación
        Project.objects.create(
            name="Proyecto Más Antiguo",
            address="Av. Antiguo 789",
            started_at="2025-01-01",
            status="Off Plan"
        )
        response = self.client.get(self.list_url, {'ordering': '-created_at'},  **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['name'], "Proyecto Más Antiguo")  # El proyecto más antiguo debería aparecer primero

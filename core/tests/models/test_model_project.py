from django.test import TestCase
from core.models.models import Project
from django.core.exceptions import ValidationError
from datetime import date


class ProjectModelTest(TestCase):
    def test_create_project(self):
        """Prueba que se pueda crear un proyecto válido"""
        project = Project.objects.create(
            name="Proyecto Test",
            address="Av. Ejemplo 123",
            started_at=date(2023, 1, 1),
            status="Off Plan"
        )
        self.assertEqual(str(project), "Proyecto Test")
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

    def test_cannot_mark_finished_without_finished_at(self):
        """Prueba que no se pueda marcar como 'Finished' sin fecha de finalización"""
        project = Project(
            name="Proyecto Erróneo",
            address="Av. Ejemplo 456",
            started_at=date(2023, 1, 1),
            status="Finished"
        )
        with self.assertRaises(ValidationError):
            project.full_clean()

    def test_autoset_status_to_finished(self):
        """Prueba que el estado cambie automáticamente a 'Finished' si tiene fecha de finalización"""
        project = Project.objects.create(
            name="Proyecto Test",
            address="Av. Ejemplo 123",
            started_at=date(2023, 1, 1),
            finished_at=date(2023, 12, 31)
        )
        self.assertEqual(project.status, "Finished")

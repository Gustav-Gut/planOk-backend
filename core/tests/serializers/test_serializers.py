from django.test import TestCase
from core.serializers.serializers import ProjectSerializer
from rest_framework.exceptions import ValidationError

class ProjectSerializerTest(TestCase):
    def test_valid_project_creation(self):
        """Prueba que se pueda crear un proyecto válido usando el serializer"""
        data = {
            "name": "Proyecto Test",
            "address": "Av. Ejemplo 123",
            "started_at": "2023-01-01",
            "status": "Off Plan"
        }
        serializer = ProjectSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        project = serializer.save()
        self.assertEqual(str(project), "Proyecto Test")

    def test_cannot_mark_finished_without_finished_at(self):
        """Prueba que no se pueda marcar como 'Finished' sin fecha de finalización en el serializer"""
        data = {
            "name": "Proyecto Erróneo",
            "address": "Av. Ejemplo 456",
            "started_at": "2023-01-01",
            "status": "Finished"
        }
        serializer = ProjectSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        # Verifica que el mensaje de error esté en non_field_errors
        self.assertIn(
            "No puedes marcar un proyecto con status Finished sin asignar valor a finished_at.",
            str(context.exception.detail["non_field_errors"])
        )

    def test_autoset_status_to_finished(self):
        """Prueba que el estado cambie automáticamente a 'Finished' si tiene fecha de finalización"""
        data = {
            "name": "Proyecto Test",
            "address": "Av. Ejemplo 123",
            "started_at": "2023-01-01",
            "finished_at": "2023-12-31"
        }
        serializer = ProjectSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        project = serializer.save()
        self.assertEqual(project.status, "Finished")

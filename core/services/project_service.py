from django.core.exceptions import ObjectDoesNotExist, ValidationError
from ..models.models import Project
from ..serializers.serializers import ProjectSerializer

class ProjectService:
    @staticmethod
    def get_projects():
        return Project.objects.all().order_by('-created_at')

    @staticmethod
    def get_project_by_id(project_id):
        try:
            return Project.objects.get(id=project_id)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_project(data):
        serializer = ProjectSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        return project

    @staticmethod
    def update_project(project_id, data):
        try:
            project = Project.objects.get(id=project_id)
            for field, value in data.items():
                setattr(project, field, value)
            project.full_clean()
            project.save()
            return project
        except ObjectDoesNotExist:
            return None
        except ValidationError as e:
            raise ValidationError(f"Error de validación: {e}")

    @staticmethod
    def partial_update_project(project_id, data):
        try:
            project = Project.objects.get(id=project_id)
            for field, value in data.items():
                setattr(project, field, value)
            project.full_clean()
            project.save()
            return project
        except ObjectDoesNotExist:
            return None
        except ValidationError as e:
            raise ValidationError(f"Error de validación: {e}")

    @staticmethod
    def delete_project(project_id):
        try:
            project = Project.objects.get(id=project_id)
            project.delete()
            return True
        except ObjectDoesNotExist:
            return False

from core.models.models import Unit, Project
from rest_framework.exceptions import ValidationError
from ..serializers.serializers import UnitSerializer

class UnitService:
    @staticmethod
    def get_all_units():
        return Unit.objects.all().order_by('-created_at')

    @staticmethod
    def get_unit_by_id(unit_id):
        return Unit.objects.get(id=unit_id)

    @staticmethod
    def create_unit(data):
        serializer = UnitSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def create_multiple_units(data_list):
        serializer = UnitSerializer(data=data_list, many=True)
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        return serializer.save()

    @staticmethod
    def update_unit(unit, data):
        for key, value in data.items():
            setattr(unit, key, value)
        unit.save()
        return unit

    @staticmethod
    def delete_unit(unit):
        unit.delete()

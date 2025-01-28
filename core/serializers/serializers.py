from rest_framework import serializers
from ..models.models import Project, Unit, Customer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get("status") == "Finished" and not attrs.get("finished_at"):
            raise serializers.ValidationError("No puedes marcar un proyecto con status Finished sin asignar valor a finished_at.")

        if attrs.get("finished_at") and attrs.get("status") != "Finished":
            attrs["status"] = "Finished"

        return attrs

class UnitSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    class Meta:
        model = Unit
        fields = '__all__'

    def validate(self, data):
        unit_status = data.get('unit_status')
        customer = data.get('customer')

        # Validación 1: Una unidad en estado 'Sold' o 'Reserved' debe tener un customer asociado
        if unit_status in ['Sold', 'Reserved'] and not customer:
            raise serializers.ValidationError({
                'customer':"Una unidad en status 'Sold' o 'Reserved' siempre debe tener un Customer asociado."
            })

        # Validación 2: Si se asocia un customer, el estado de la unidad debe ser 'Sold' o 'Reserved'
        if customer and unit_status not in ['Sold', 'Reserved']:
            raise serializers.ValidationError({
                'unit_status': "Una unidad con Customer asociado solo puede tener status 'Sold' or 'Reserved'."
            })

        return data

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
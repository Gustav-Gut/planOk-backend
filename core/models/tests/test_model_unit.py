from django.test import TestCase
from core.models.models import Project, Unit, Customer
from datetime import date

class UnitModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Proyecto Test",
            address="Av. Ejemplo 123",
            started_at=date(2023, 1, 1),
            status="Off Plan"
        )

    def test_create_unit(self):
        """Prueba que se pueda crear una unidad válida"""
        unit = Unit.objects.create(
            unit_number="1A",
            unit_type="Apartment",
            square_meters=50.5,
            price=150000000,
            unit_status="Available",
            project=self.project
        )
        self.assertEqual(str(unit), f"Unit 1A - {self.project.name}")

    def test_unit_can_reference_customer(self):
        """Prueba que una unidad pueda asociarse a un cliente"""
        customer = Customer.objects.create(
            rut="12345678-9",
            name="Juan",
            lastname="Pérez",
            email="juan.perez@example.com",
            phone="+56912345678"
        )
        unit = Unit.objects.create(
            unit_number="1A",
            unit_type="Apartment",
            square_meters=50.5,
            price=150000000,
            unit_status="Available",
            project=self.project,
            customer=customer
        )
        self.assertEqual(unit.customer.name, "Juan")

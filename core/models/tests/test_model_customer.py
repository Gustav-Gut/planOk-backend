from django.test import TestCase
from core.models.models import Customer
from django.core.exceptions import ValidationError


class CustomerModelTest(TestCase):
    def test_create_customer(self):
        """Prueba que se pueda crear un cliente válido"""
        customer = Customer.objects.create(
            rut="12345678-9",
            name="Juan",
            lastname="Pérez",
            email="juan.perez@example.com",
            phone="+56912345678"
        )
        self.assertEqual(str(customer), "Juan Pérez")

    def test_unique_rut_and_email(self):
        """Prueba que no se puedan duplicar RUT o email"""
        Customer.objects.create(
            rut="12345678-9",
            name="Juan",
            lastname="Pérez",
            email="juan.perez@example.com",
            phone="+56912345678"
        )
        with self.assertRaises(ValidationError):
            customer = Customer(
                rut="12345678-9",
                name="Pedro",
                lastname="Gómez",
                email="pedro.gomez@example.com"
            )
            customer.full_clean()

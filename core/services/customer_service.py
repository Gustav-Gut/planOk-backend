from core.models.models import Customer
from core.serializers.serializers import CustomerSerializer

class CustomerService:
    @staticmethod
    def get_all_customers():
        return Customer.objects.all().order_by('-created_at')

    @staticmethod
    def get_customer_by_id(customer_id):
        return Customer.objects.get(id=customer_id)

    @staticmethod
    def create_customer(data):
        serializer = CustomerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def update_customer(customer, data, partial=False):
        serializer = CustomerSerializer(customer, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @staticmethod
    def delete_customer(customer):
        customer.delete()

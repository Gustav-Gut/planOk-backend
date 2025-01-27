import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Project(models.Model):
    PROJECT_STATUS = (
        ('Off Plan', 'Off Plan'),
        ('Under Construction', 'Under Construction'),
        ('Finished', 'Finished'),
        ('Sold', 'Sold'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    started_at = models.DateField()
    finished_at = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS, default="Off Plan")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Si se marca como Finished sin tener finished_at
        if self.status == 'Finished' and not self.finished_at:
            raise ValidationError(
                "Cannot mark project as 'Finished' without a 'finished_at' date."
            )

        super().clean()

    def save(self, *args, **kwargs):
        # Si tenemos finished_at y no está en 'Finished', forzamos el status
        if self.finished_at and self.status != 'Finished':
            self.status = 'Finished'

        # Antes de hacer el .save(), pasamos por clean() para asegurarnos que no viole la validación
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    rut = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.lastname}"


class Unit(models.Model):
    UNIT_STATUS = (
        ('Available', 'Available'),
        ('Sold', 'Sold'),
        ('Reserved', 'Reserved'),
    )
    UNIT_TYPE = (
        ('Apartment', 'Apartment'),
        ('House', 'House'),
        ('Office', 'Office'),
        ('Commercial', 'Commercial'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    project = models.ForeignKey(
        Project,
        related_name='units',
        on_delete=models.CASCADE
    )
    client = models.ForeignKey(
        Client,
        related_name='units',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    unit_number = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50, choices=UNIT_TYPE)
    square_meters = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.IntegerField()
    reservation_deposit = models.IntegerField(default=0)
    unit_status = models.CharField(max_length=50, choices=UNIT_STATUS, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Unit {self.unit_number} - {self.project.name}"

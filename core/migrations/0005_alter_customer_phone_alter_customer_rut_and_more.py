# Generated by Django 5.1.5 on 2025-01-27 22:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_client_customer_rename_client_unit_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.MinLengthValidator(12)]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='rut',
            field=models.CharField(max_length=9, unique=True, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('Off Plan', 'Off Plan'), ('Under Construction', 'Under Construction'), ('Finished', 'Finished'), ('Sold', 'Sold')], default='Off Plan', max_length=20),
        ),
        migrations.AlterField(
            model_name='unit',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='unit',
            name='square_meters',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_number',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_status',
            field=models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold'), ('Reserved', 'Reserved')], default='Available', max_length=20),
        ),
        migrations.AlterField(
            model_name='unit',
            name='unit_type',
            field=models.CharField(choices=[('Apartment', 'Apartment'), ('House', 'House'), ('Office', 'Office'), ('Commercial', 'Commercial')], max_length=20),
        ),
    ]

# Generated by Django 4.1.3 on 2024-11-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_shipment_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='fullname',
            field=models.CharField(max_length=100),
        ),
    ]

# Generated by Django 4.1.3 on 2024-10-15 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_cart',
            name='product_qty',
            field=models.IntegerField(default=1),
        ),
    ]
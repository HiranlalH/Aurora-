# Generated by Django 4.1.3 on 2024-10-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=50)),
                ('message', models.TextField()),
            ],
        ),
    ]

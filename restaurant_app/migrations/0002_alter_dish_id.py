# Generated by Django 4.2.4 on 2023-08-15 08:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='id',
            field=models.UUIDField(default=uuid.UUID('c56a7613-5dae-4cd6-a081-b371b81fe96d'), editable=False, primary_key=True, serialize=False),
        ),
    ]

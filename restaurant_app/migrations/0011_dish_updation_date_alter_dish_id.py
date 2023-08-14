# Generated by Django 4.2.4 on 2023-08-13 10:34

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0010_alter_dish_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='updation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dish',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e2fd34d1-9fe5-44fb-8d4c-fbf6b6993a24'), editable=False, primary_key=True, serialize=False),
        ),
    ]

# Generated by Django 4.2.4 on 2023-08-13 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0008_alter_dish_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
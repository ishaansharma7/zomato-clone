# Generated by Django 4.2.4 on 2023-08-14 12:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email Address')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=3, message='Username should be atleast 3 characters')])),
                ('full_name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(limit_value=3, message='Name should be atleast 3 characters')])),
                ('contact_number', models.CharField(max_length=10)),
                ('address', models.TextField(validators=[django.core.validators.MinLengthValidator(limit_value=3, message='Address should be atleast 5 characters')])),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('restaurant_manager', 'Restaurant Manager')], default='customer', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

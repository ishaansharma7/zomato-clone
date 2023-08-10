from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, username, full_name, contact_number, password=None, address):
#         if not email:
#             raise ValueError('email required!!')
        
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, full_name=full_name, contact_number=contact_number, address)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, username, full_name, contact_number, password=None, address):
#         user = self.create_user(email=email, username=username, full_name=full_name, contact_number=contact_number, password=password, address=address)
#         user.is_staff = True
#         user.is_superuser = True
#         user.save()
#         return user


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, full_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must have staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have superuser=True')
        return self.create_user(email, username, full_name, password, **other_fields)

    def create_user(self, email, username, full_name, password, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True,
                    validators=[MinLengthValidator(limit_value=3, message='Username should be atleast 3 characters')])
    full_name = models.CharField(max_length=255,
                                validators=[MinLengthValidator(limit_value=3, message='Name should be atleast 3 characters')])
    contact_number = models.CharField(max_length=10)
    address = models.TextField(validators=[MinLengthValidator(limit_value=3, message='Address should be atleast 5 characters')])
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('restaurant', 'Restaurant')
    )
    user_type = models.CharField(choices=TYPE_CHOICES, default='customer', max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name', 'contact_number']

    def __str__(self):
        return self.email
    

    def clean(self):

        if not self.contact_number.isdigit() or len(self.contact_number) != 10:
            raise ValidationError('Please enter 10 digit contact number')
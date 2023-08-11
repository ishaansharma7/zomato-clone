from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


class RestaurantDetail(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField(unique=True, validators=[
        MinLengthValidator(limit_value=5, message='Address should be atleast 5 characters long')])
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(validators=[MinValueValidator(limit_value=20), MaxValueValidator(limit_value=3000)])
    description = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey(RestaurantDetail, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Cart(models.Model):
    cart_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_placed = models.BooleanField(default=False)

    def __str__(self):
        return self.cart_owner


class OrderDetail(models.Model):
    placed_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, default=None)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, default=None)
    quantity = models.IntegerField(validators=[MinValueValidator(limit_value=0), MaxValueValidator(5)])
    total_price = models.DecimalField()


    def __str__(self):
        return self.placed_by
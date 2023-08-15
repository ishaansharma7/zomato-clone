from django.contrib import admin
from .models import RestaurantDetail, Dish, OrderDetail, Cart


admin.site.register(RestaurantDetail)
admin.site.register(Dish)
admin.site.register(OrderDetail)
admin.site.register(Cart)
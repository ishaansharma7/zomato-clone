from django.urls import path
from .views import DishListing, add_item, remove_item, cart_listing

app_name = 'restaurant_app'

urlpatterns = [
    path('home/', DishListing.as_view(), name='dish_listing'),
    path('add-item/<int:page>/<str:dish_id>/<str:dish_name>', add_item, name='add_item'),
    path('remove-item/<int:page>/<str:dish_id>/<str:dish_name>', remove_item, name='remove_item'),
    path('cart/', cart_listing, name='cart_listing')
]
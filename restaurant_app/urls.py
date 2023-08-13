from django.urls import path
from .views import DishListing, add_item

app_name = 'restaurant_app'

urlpatterns = [
    path('home/', DishListing.as_view(), name='dish_listing'),
    path('add-item/<int:page>/<str:dish_id>/<str:dish_name>', add_item, name='add_item'),
]
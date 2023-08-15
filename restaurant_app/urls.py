from django.urls import path
from .views import (DishListing, add_item, remove_item, cart_listing, add_item_cart,
                    remove_item_cart, place_order, OrderHistory, order_history, analytics)

app_name = 'restaurant_app'

urlpatterns = [
    path('home/', DishListing.as_view(), name='dish_listing'),

    path('add-item/<int:page>/<str:dish_id>/<str:dish_name>/', add_item, name='add_item'),
    path('add-item/<int:page>/<str:dish_id>/<str:dish_name>/<str:search_term>', add_item, name='add_item'),

    path('remove-item/<int:page>/<str:dish_id>/<str:dish_name>/', remove_item, name='remove_item'),
    path('remove-item/<int:page>/<str:dish_id>/<str:dish_name>/<str:search_term>', remove_item, name='remove_item'),

    path('add-item-cart/<str:dish_id>/<str:dish_name>', add_item_cart, name='add_item_cart'),
    path('remove-item-cart/<str:dish_id>/<str:dish_name>', remove_item_cart, name='remove_item_cart'),

    path('cart/', cart_listing, name='cart_listing'),
    path('place-order/', place_order, name='place_order'),

    path('past-orders/', order_history, name='past_orders'),
    path('analytics/', analytics, name='analytics'),
]
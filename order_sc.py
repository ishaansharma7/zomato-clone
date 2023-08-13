from restaurant_app.models import Dish, OrderDetail, Cart
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


def add_order(user, dish_pk):
    dish = Dish.objects.get(pk=dish_pk)
    order, created = OrderDetail.objects.get_or_create(placed_by=user, dish=dish)
    if created:
        order.total_price = dish.price
        print('order created')
    else:
        order.quantity += 1
        order.total_price += dish.price
        print('added quantity in order')
    order.save()


def subtract_order(user, dish_pk):
    dish = Dish.objects.get(pk=dish_pk)
    try:
        order = OrderDetail.objects.get(dish=dish, placed_by=user)
    except ObjectDoesNotExist:
        print('no order exist')
        return
    
    if order.quantity > 1:
        order.total_price = dish.price*order.quantity
        order.quantity -= 1
        order.total_price -= dish.price
        order.save()
        print('removed quantity')
    elif order.quantity == 1:
        order.delete()
        print('removed dish')
    else:
        print('this case should not occur logically')
    

def execute():
    ishaan = CustomUser.objects.get(username='ishaan7')
    dish = Dish.objects.filter(name__icontains='cheese')[0]
    # add_order(user=ishaan, dish_pk=dish.id)
    subtract_order(user=ishaan, dish_pk=dish.id)
    print('operation done')

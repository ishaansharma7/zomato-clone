from .models import OrderDetail
from datetime import datetime, timedelta
import pytz

def add_item_operation(request, dish_id, dish_name):
    user_email = request.user.email
    # dish_id = int(dish_id)
    if 'cart_session' not in request.session:
        request.session['cart_session'] = {}
    if user_email not in request.session['cart_session']:
        request.session['cart_session'][user_email] = {}
        request.session['cart_session'][user_email][dish_id] = 1
        request.session['dish_operation'] = dish_name + ' added to cart!'
        print('r1')
    else:
        if dish_id in request.session['cart_session'][user_email]:
            if request.session['cart_session'][user_email][dish_id] == 5:
                request.session['dish_operation'] = 'Limit exceeded!'
                print('r2')
            else:
                request.session['cart_session'][user_email][dish_id] += 1
                request.session['dish_operation'] = dish_name + ' added to cart!'
                print('r3')
        else:
            request.session['cart_session'][user_email][dish_id] = 1
            request.session['dish_operation'] = dish_name + ' added to cart!'
            print('r4')
    request.session.save()


def remove_item_operation(request, dish_id, dish_name):
    user_email = request.user.email
    if 'cart_session' not in request.session:
        request.session['cart_session'] = {}
    if user_email not in request.session['cart_session']:
        print('never added any item')
    else:
        if dish_id in request.session['cart_session'][user_email]:
            if request.session['cart_session'][user_email][dish_id] == 1:
                request.session['cart_session'][user_email].pop(dish_id)
                request.session['dish_operation'] = dish_name +' removed from cart'
            else:
                request.session['cart_session'][user_email][dish_id] -= 1
                request.session['dish_operation'] = dish_name +' removed from cart'
        else:
            print('this item was not added before')
    request.session.save()


def create_order_from_session(matching_dishes, session_dishes_dict, user):
    for dish in matching_dishes:
        quantity = session_dishes_dict[str(dish.id)]
        total_price = round(quantity * dish.price, 2)
        OrderDetail.objects.create(placed_by=user, dish=dish, quantity=quantity, total_price=total_price, order_placed=True)


def get_date_range(duration):
    print(duration)
    ist_timezone = pytz.timezone('UTC')
    # ist_timezone = pytz.timezone('Asia/Kolkata')
    if duration == 'Past 1 day':
        current = datetime.now().astimezone(ist_timezone)
        before = current - timedelta(days=1)
        before = before.replace(hour=0, minute=0, second=0, microsecond=0)
        return current, before
    elif duration == 'Past 3 days':
        current = datetime.now().astimezone(ist_timezone)
        before = current - timedelta(days=3)
        before = before.replace(hour=0, minute=0, second=0, microsecond=0)
        return current, before
    elif duration == 'Past week':
        current = datetime.now().astimezone(ist_timezone)
        before = current - timedelta(days=7)
        before = before.replace(hour=0, minute=0, second=0, microsecond=0)
        return current, before
    elif duration == 'Past month':
        current = datetime.now().astimezone(ist_timezone)
        before = current - timedelta(days=30)
        before = before.replace(hour=0, minute=0, second=0, microsecond=0)
        return current, before
    elif duration == 'Past year':
        current = datetime.now().astimezone(ist_timezone)
        before = current - timedelta(days=365)
        before = before.replace(hour=0, minute=0, second=0, microsecond=0)
        return current, before
    return None, None
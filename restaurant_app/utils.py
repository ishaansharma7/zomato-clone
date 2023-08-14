def add_item_operation(request, dish_id, dish_name):
    user_email = request.user.email
    # dish_id = int(dish_id)
    if 'cart_session' not in request.session:
        request.session['cart_session'] = {}
    if user_email not in request.session['cart_session']:
        request.session['cart_session'][user_email] = {}
        request.session['cart_session'][user_email][dish_id] = 1
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
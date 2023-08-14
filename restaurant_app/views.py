from django.views.generic import ListView
from django.shortcuts import render
from .models import Dish
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class DishListing(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'restaurant_app/dish_listing.html'
    context_object_name = 'dish'
    paginate_by = 5
    
    def get_queryset(self):
        return super().get_queryset().order_by('-id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search_term')
        if search_term is not None:
            queryset = self.get_queryset().filter(Q(name__icontains=search_term) | Q(restaurant__name__icontains=search_term))
        else:
            queryset = self.get_queryset()
        
        # pagination logic
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        # message logic
        if self.request.session.get('dish_operation'):
            messages.success(self.request, self.request.session.get('dish_operation'))
            self.request.session.pop('dish_operation')

        # item logic
        user_email = self.request.user.email
        if 'cart_session' in self.request.session and user_email in self.request.session['cart_session']:
            context['quantity'] = dict(self.request.session['cart_session'][user_email])
        return context


@login_required(login_url='accounts_app:login')
def add_item(request, page, dish_id, dish_name):
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
    # pprint(dict(request.session), indent=2)
    url = reverse('restaurant_app:dish_listing') + f'?page={page}'
    return redirect(url)


@login_required(login_url='accounts_app:login')
def remove_item(request, page, dish_id, dish_name):
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
    # pprint(dict(request.session), indent=2)
    url = reverse('restaurant_app:dish_listing') + f'?page={page}'
    return redirect(url)


@login_required(login_url='accounts_app:login')
def cart_listing(request):
    cart_session = request.session.get('cart_session')
    user_email = request.user.email
    session_dishes_dict = {}
    if cart_session and user_email in cart_session:
        session_dishes_dict = cart_session[user_email]
    
    matching_dishes = Dish.objects.filter(id__in=session_dishes_dict.keys())
    context = {'cart_dishes': matching_dishes}
    return render(request, 'restaurant_app/cart_listing.html', context)
    

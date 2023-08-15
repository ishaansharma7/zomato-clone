from typing import Any, Dict
from django.db.models.query import QuerySet
from django.views.generic import ListView, FormView
from django.shortcuts import render
from .models import Dish, OrderDetail
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from restaurant_app.utils import add_item_operation, remove_item_operation, create_order_from_session, get_date_range


class DishListing(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'restaurant_app/dish_listing.html'
    context_object_name = 'dish'
    paginate_by = 5
    
    def get_queryset(self):
        return super().get_queryset().order_by('-updation_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_term = self.request.GET.get('search_term')
        if search_term is not None and search_term not in ['', 'none']:
            print('rann----')
            context['search_term'] = search_term
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
            self.request.session.save()

        # item logic
        user_email = self.request.user.email
        if 'cart_session' in self.request.session and user_email in self.request.session['cart_session']:
            context['quantity'] = dict(self.request.session['cart_session'][user_email])
            pprint(context['quantity'], indent=2)
        return context


@login_required(login_url='accounts_app:login')
def add_item(request, page, dish_id, dish_name, search_term='none'):
    add_item_operation(request, dish_id, dish_name)
    # pprint(dict(request.session), indent=2)
    if search_term != 'none':
        url = reverse('restaurant_app:dish_listing') + f'?page={page}&search_term={search_term}'
    else:
        url = reverse('restaurant_app:dish_listing') + f'?page={page}'
    return redirect(url)


@login_required(login_url='accounts_app:login')
def remove_item(request, page, dish_id, dish_name, search_term='none'):
    remove_item_operation(request, dish_id, dish_name)
    # pprint(dict(request.session), indent=2)
    if search_term != 'none':
        url = reverse('restaurant_app:dish_listing') + f'?page={page}&search_term={search_term}'
    else:
        url = reverse('restaurant_app:dish_listing') + f'?page={page}'
    return redirect(url)


@login_required(login_url='accounts_app:login')
def add_item_cart(request, dish_id, dish_name):
    add_item_operation(request, dish_id, dish_name)
    # pprint(dict(request.session), indent=2)
    url = reverse('restaurant_app:cart_listing')
    return redirect(url)


@login_required(login_url='accounts_app:login')
def remove_item_cart(request, dish_id, dish_name):
    remove_item_operation(request, dish_id, dish_name)
    # pprint(dict(request.session), indent=2)
    url = reverse('restaurant_app:cart_listing')
    return redirect(url)


@login_required(login_url='accounts_app:login')
def cart_listing(request):
    session_dishes_dict = {}
    user_email = request.user.email
    cart_session = request.session.get('cart_session')
    if cart_session and user_email in cart_session:
        session_dishes_dict = cart_session[user_email]
    
    matching_dishes = Dish.objects.filter(id__in=session_dishes_dict.keys())
    context = {'cart_dishes': matching_dishes}

    if 'cart_session' in request.session and user_email in request.session['cart_session']:
        context['quantity'] = dict(request.session['cart_session'][user_email])
    
    # message logic
    if request.session.get('dish_operation'):
        messages.success(request, request.session.get('dish_operation'))
        request.session.pop('dish_operation')
    
    return render(request, 'restaurant_app/cart_listing.html', context)


@login_required(login_url='accounts_app:login')
def place_order(request):
    session_dishes_dict = {}
    user_email = request.user.email
    cart_session = request.session.get('cart_session')
    if cart_session and user_email in cart_session:
        session_dishes_dict = cart_session[user_email]
    else:
        print('cart_session or email not available')
        return redirect('restaurant_app:sih_listing')
    
    matching_dishes = Dish.objects.filter(id__in=session_dishes_dict.keys())
    create_order_from_session(matching_dishes, session_dishes_dict, request.user)
    request.session['cart_session'].pop(user_email)
    request.session.save()
    return render(request, 'restaurant_app/order_confirmed.html')
        

class OrderHistory(LoginRequiredMixin, ListView, ):
    model = OrderDetail
    template_name = 'restaurant_app/order_history.html'
    context_object_name = 'ordered_dishes'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().order_by('-order_time')
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.method == 'POST':
            print('R1')
            queryset = self.get_queryset().filter(placed_by=user, order_placed=True)
        else:
            queryset = self.get_queryset().filter(placed_by=user, order_placed=True)
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj


        return context


@login_required(login_url='accounts_app:login')
def order_history(request):
    user = request.user
    paginate_by = 5
    context = {}
    if request.GET.get('duration') and request.GET['duration'] != 'All orders':
        duration = request.GET.get('duration')
        context['selected_duration'] = duration
        range1, range2 = get_date_range(duration)
        # print(range1, range2)
        queryset = OrderDetail.objects.filter(placed_by=user, order_placed=True, order_time__range=(range2, range1)).order_by('-order_time')
    else:
        queryset = OrderDetail.objects.filter(placed_by=user, order_placed=True).order_by('-order_time')
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, 'restaurant_app/order_history.html', context)
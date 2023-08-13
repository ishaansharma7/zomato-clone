from django.views.generic import ListView
from .models import Dish
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class DishListing(ListView):
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
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        if self.request.session.get('item_added'):
            messages.success(self.request, self.request.session.get('item_added') + ' added to cart!')
            self.request.session.pop('item_added')
        return context


def add_item(request, page, dish_id, dish_name):
    user = request.user
    print(user)
    print(dish_id)
    request.session['item_added'] = dish_name
    url = reverse('restaurant_app:dish_listing') + f'?page={page}'
    return redirect(url)
    # return DishListing.as_view()
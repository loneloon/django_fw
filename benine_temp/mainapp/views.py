from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import datetime
import json
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket

from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
# Create your views here.

date = str(datetime.datetime.now().strftime('%d.%m.%Y'))


def get_links_menu():
   if settings.LOW_CACHE:
       key = 'links_menu'
       links_menu = cache.get(key)
       if links_menu is None:
           links_menu = ProductCategory.objects.filter(is_active=True)
           cache.set(key, links_menu)
       return links_menu
   else:
       return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
   if settings.LOW_CACHE:
       key = f'category_{pk}'
       category = cache.get(key)
       if category is None:
           category = get_object_or_404(ProductCategory, pk=pk)
           cache.set(key, category)
       return category
   else:
       return get_object_or_404(ProductCategory, pk=pk)


def get_products():
   if settings.LOW_CACHE:
       key = 'products'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, 
                         category__is_active=True).select_related('category')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True, 
                         category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Product, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
   if settings.LOW_CACHE:
       key = 'products_orederd_by_price'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(is_active=True, 
                                  category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(is_active=True,
                                 category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
   if settings.LOW_CACHE:
       key = f'products_in_category_orederd_by_price_{pk}'
       products = cache.get(key)
       if products is None:
           products = Product.objects.filter(category__pk=pk, is_active=True,
                              category__is_active=True).order_by('price')
           cache.set(key, products)
       return products
   else:
       return Product.objects.filter(category__pk=pk, is_active=True, 
                              category__is_active=True).order_by('price')


def fetch_basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket.select_related().all()

    return basket


def fetch_pages(page, content, offset):

    paginator = Paginator(content, offset)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    return pages


def fetch_amount(basket):
    b_count = 0

    if basket:
        for item in basket:
            b_count += item.quantity
    return b_count


def fetch_sum(basket):
    b_sum = 0

    if basket:
        for item in basket:
            b_sum += item.product.price * item.quantity
    return b_sum

def index(request):


    context = {
        'page_title':'home',
    }

    return render(request, 'mainapp/index.html', context)


@cache_page(3600)
def products(request):


    categories = get_links_menu()
    products = get_products()

    context = {
        'page_title': 'products',
        'categories': categories,
        'products': products,

    }

    return render(request, 'mainapp/products.html', context)



@never_cache
def category_products(request, pk=None, page=1):


    categories = get_links_menu()
    
    if pk is not None:
        if pk == 0:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).order_by('id')
            category = {'pk':0, 'name': 'All'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk,
                                              is_active=True, category__is_active=True).order_by('id')

        products_paginator = fetch_pages(page, products, 3)

        context = {
                    'page_title': 'products',
                    'categories': categories,
                    'products': products_paginator,
                    'category': category,
                }

        return render(request, 'mainapp/products.html', context)

    return render(request, 'mainapp/products.html')


# def products_ajax(request, pk=None, page=1):
#   if request.is_ajax():
#     links_menu = get_links_menu()

#     if pk:
#       if pk == '0':
#           category = {
#               'pk': 0,
#               'name': 'All'
#           }
#           products = get_products_orederd_by_price()
#       else:
#           category = get_category(pk)
#           products = get_products_in_category_orederd_by_price(pk)

#       paginator = Paginator(products, 2)
#       try:
#         products_paginator = paginator.page(page)
#       except PageNotAnInteger:
#         products_paginator = paginator.page(1)
#       except EmptyPage:
#         products_paginator = paginator.page(paginator.num_pages)

#       categories = get_links_menu()

#       content = {
#         'links_menu': links_menu,
#         'categories': categories,
#         'category': category,
#         'products': products_paginator,
#       }

#       result = render_to_string(
#                   'mainapp/includes/inc__p_all.html',
#                   context=content,
#                   request=request)
#       return JsonResponse({'result': result})



def product_inspect(request, pk=None, last_page=None):


    if pk is not None:
        product = get_object_or_404(Product, pk=pk)

        context = {
            'page_title': 'products',
            'product': product,
            'last_page': last_page,
        }
        return render(request, 'mainapp/products.html', context)

    else:
        return products(request)


def contacts(request):


    context = {
        'page_title': 'contacts'
    }

    try:
        with open('mainapp/json/offices.json', 'r') as off_json:
            locations = json.load(off_json)['offices']['locations']
        context['locations'] = locations
    except:
        print('JSON file was not found.')
        pass


    return render(request, 'mainapp/contacts.html', context)


def product_detail_async(request, pk):
    if request.is_ajax():
        try:
            product = Product.objects.get(pk=pk)
            return JsonResponse({
                'product_price': product.price
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            })

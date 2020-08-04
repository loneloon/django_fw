from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
import json
from mainapp.models import ProductCategory, Product
from basketapp.models import Basket

# Create your views here.

date = str(datetime.datetime.now().strftime('%d.%m.%Y'))


def fetch_basket(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

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



def products(request):


    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'products',
        'categories': categories,
        'products': products,

    }

    return render(request, 'mainapp/products.html', context)


def category_products(request, pk=None, page=1):


    categories = ProductCategory.objects.filter(is_active=True)

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

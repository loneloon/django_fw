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

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    context = {
        'page_title':'home',
        'basket': basket,
        'b_count': b_count,
        'b_sum': b_sum,
    }

    return render(request, 'mainapp/index.html', context)



def products(request):

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    categories = ProductCategory.objects.all()
    products = Product.objects.all()

    context = {
        'page_title': 'products',
        'categories': categories,
        'products': products,
        'basket': basket,
        'b_count': b_count,
        'b_sum': b_sum,

    }

    return render(request, 'mainapp/products.html', context)


def category_products(request, pk=None, page=1):

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('id')
            category = {'pk':0, 'name': 'All'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('id')

        products_paginator = fetch_pages(page, products, 3)

        context = {
                    'page_title': 'products',
                    'categories': categories,
                    'products': products_paginator,
                    'category': category,
                    'basket': basket,
                    'b_count': b_count,
                    'b_sum': b_sum,
                }

        return render(request, 'mainapp/products.html', context)

    return render(request, 'mainapp/products.html')


def product_inspect(request, pk=None, last_page=None):

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    if pk is not None:
        product = get_object_or_404(Product, pk=pk)

        context = {
            'page_title': 'products',
            'product': product,
            'basket': basket,
            'last_page': last_page,
            'b_count': b_count,
            'b_sum': b_sum,
        }
        return render(request, 'mainapp/products.html', context)

    else:
        return products(request)


def contacts(request):

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    context = {
        'page_title': 'contacts',
        'basket': basket,
        'b_count': b_count,
        'b_sum': b_sum,
    }

    try:
        with open('mainapp/json/offices.json', 'r') as off_json:
            locations = json.load(off_json)['offices']['locations']
        context['locations'] = locations
    except:
        print('JSON file was not found.')
        pass


    return render(request, 'mainapp/contacts.html', context)



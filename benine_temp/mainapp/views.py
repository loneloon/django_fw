from django.shortcuts import render
import datetime
import json
from mainapp.models import ProductCategory, Product

# Create your views here.

date = str(datetime.datetime.now().strftime('%d.%m.%Y'))


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


def contacts(request):
    context = {
        'page_title': 'contacts',
    }

    try:
        with open('mainapp/json/offices.json', 'r') as off_json:
            locations = json.load(off_json)['offices']['locations']
        context['locations'] = locations
    except:
        print('JSON file was not found.')
        pass


    return render(request, 'mainapp/contacts.html', context)



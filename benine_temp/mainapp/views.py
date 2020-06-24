from django.shortcuts import render
import datetime
import json

# Create your views here.

date = str(datetime.datetime.now().strftime('%d.%m.%Y'))


def index(request):

    context = {
        'page_title':'home',
        'cur_date': f'{date}',
        'cur_year': f'{date[-4:]}',
    }

    return render(request, 'mainapp/index.html', context)

def products(request):

    context = {
        'page_title': 'products',
        'cur_date': f'{date}',
        'cur_year': f'{date[-4:]}',
    }

    return render(request, 'mainapp/products.html', context)

def contacts(request):
    context = {
        'page_title': 'contacts',
        'cur_date': f'{date}',
        'cur_year': f'{date[-4:]}',
    }

    try:
        with open('static/json/offices.json', 'r') as off_json:
            locations = json.load(off_json)['offices']['locations']
        context['locations'] = locations
    except:
        print('JSON file was not found.')
        pass


    return render(request, 'mainapp/contacts.html', context)



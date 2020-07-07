from django.contrib import admin
from django.urls import path, include

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('catalog/', mainapp.products, name='products'),
    path('products/', mainapp.products, name='products'),
    path('category/<int:pk>/products', mainapp.category_products, name='category_products'),
    path('catalog/<int:pk>', mainapp.product_inspect, name='product_inspect'),
    path('contacts/', mainapp.contacts, name='contacts'),
]
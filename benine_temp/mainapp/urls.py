from django.contrib import admin
from django.urls import path, include

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('catalog/', mainapp.products, name='products'),
    path('products/', mainapp.products, name='products'),
    path('category/<int:pk>/page/<int:page>', mainapp.category_products, name='category_products'),
    path('category/<int:pk>/page/<int:page>', mainapp.category_products, name='page'),
    path('catalog/<int:pk>/page/<int:last_page>', mainapp.product_inspect, name='product_inspect'),
    path('product/detail/<int:pk>/async/', mainapp.product_detail_async),
    path('contacts/', mainapp.contacts, name='contacts'),
]
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('catalog/', mainapp.products, name='products'),
    path('products/', mainapp.products, name='products'),
    path('category/<int:pk>/page/<int:page>', mainapp.category_products, name='category_products'),
    re_path(r'^category/(?P<pk>\d+)/$', cache_page(3600)(mainapp.products)),
    # re_path(r'^category/(?P<pk>\d+)/ajax/$',
    #        cache_page(3600)(mainapp.products_ajax)),
    # re_path(r'^category/(?P<pk>\d+)/page/(?P<page>\d+)/ajax/$',
    #        cache_page(3600)(mainapp.products_ajax)),
    path('category/<int:pk>/page/<int:page>', mainapp.category_products, name='page'),
    path('catalog/<int:pk>/page/<int:last_page>', mainapp.product_inspect, name='product_inspect'),
    path('product/detail/<int:pk>/async/', mainapp.product_detail_async),
    path('contacts/', mainapp.contacts, name='contacts'),
]
from django.contrib import admin
from django.urls import path, include

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('verification/<str:email>/<str:activation_key>/', authapp.verify, name='verify')
]
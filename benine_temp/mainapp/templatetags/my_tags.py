from django import template
from django.conf import settings

register = template.Library()


def media_folder_products(string):

    if not string:
        string = 'img/prods/default.png'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_folder_users')
def media_folder_users(string):

    if not string:
        string = 'users_pictures/user_pic.png'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_folder_products', media_folder_products)


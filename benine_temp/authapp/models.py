from django.db import models

from django.contrib.auth.models import User, AbstractUser


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='age', null=True)
    profile_pic = models.ImageField(upload_to='users_pictures', blank=True)


from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from django.contrib.auth.models import User, AbstractUser

from datetime import timedelta
from django.utils.timezone import now
from django.urls import reverse


def get_expiration_date():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    age = models.PositiveSmallIntegerField(verbose_name='age', null=True)
    profile_pic = models.ImageField(upload_to='users_pictures', blank=True)

    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expiration = models.DateTimeField(default=get_expiration_date)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expiration

    def send_verify_mail(self):
        verify_link = reverse('auth:verify',
                              kwargs={'email': self.email, 'activation_key': self.activation_key})

        title = f'Подтверждение учетной записи {self.username}'


        message = f'Для подтверждения учетной записи {self.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(title, message, settings.EMAIL_HOST_USER, [self.email], fail_silently=False)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)



class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'F'),
    )

    user = models.OneToOneField(ShopUser, primary_key=True, null=False,
                                db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='tags', max_length=128,
                               blank=True)
    aboutMe = models.TextField(verbose_name='about', max_length=512,
                               blank=True)
    gender = models.CharField(verbose_name='gender', max_length=1,
                              choices=GENDER_CHOICES, blank=True)


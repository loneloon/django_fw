from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from mainapp.views import fetch_basket, fetch_amount, fetch_sum
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


@login_required
def basket(request):
    return render(request, 'basketapp/cart.html')


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product_inspect', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product_inspect', args=[pk]))

    basket_inst = get_object_or_404(Basket, pk=pk)

    if basket_inst.quantity <= 1:
        basket_inst.delete()
    else:
        basket_inst.quantity -= 1
        basket_inst.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_clear(request):
    basket = Basket.objects.filter(user=request.user)

    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# @receiver(pre_save, sender=OrderItem)
@receiver(pre_save, sender=Basket)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
   if update_fields is 'quantity' or 'product':
       if instance.pk:
           instance.product.stock -= instance.quantity - sender.get_item(instance.pk).quantity
       else:
           instance.product.stock -= instance.quantity
       instance.product.save()


# @receiver(pre_delete, sender=OrderItem)
@receiver(pre_delete, sender=Basket)
def product_quantity_update_delete(sender, instance, **kwargs):
   instance.product.stock += instance.quantity
   instance.product.save()
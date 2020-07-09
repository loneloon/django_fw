from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from basketapp.models import Basket
from mainapp.models import Product
from mainapp.views import fetch_basket, fetch_amount, fetch_sum
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def basket(request):

    basket = fetch_basket(request)

    b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    content = {
        'page_title': 'cart',
        'basket': basket,
        'b_count': b_count,
        'b_sum': b_sum,
    }
    return render(request, 'basketapp/cart.html', content)


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
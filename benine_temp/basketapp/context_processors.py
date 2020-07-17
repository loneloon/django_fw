from mainapp.views import fetch_basket, fetch_amount, fetch_sum


def basket(request):

    if request.user.is_authenticated:
        basket = fetch_basket(request)
        b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    else:
        basket = []
        b_count, b_sum = fetch_amount(basket), fetch_sum(basket)

    return {
        'basket': basket,
        'b_count': b_count,
        'b_sum': b_sum,
    }
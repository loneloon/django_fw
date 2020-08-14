from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Forming'),
        (SENT_TO_PROCEED, 'In progress'),
        (PAID, 'Paid'),
        (PROCEEDED, 'Processing'),
        (READY, 'Ready for pickup'),
        (CANCEL, 'Canceled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='updated', auto_now=True)
    status = models.CharField(verbose_name='status',
                              max_length=3,
                              choices=ORDER_STATUS_CHOICES,
                              default=FORMING)
    is_active = models.BooleanField(verbose_name='active', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return 'Current order: {}'.format(self.id)

    def get_total_quantity(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitem.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitem.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def get_summary(self):
    	items = self.orderitem.select_related()
    	return {
    		'total_cost': sum(list(map(lambda x: x.quantity * x.product.price. items))),
    		'total_quantity': sum(list(map(lambda x: x.quantity, items)))
    	}

    # переопределяем метод, удаляющий объект
    def delete(self, *kwargs):
        for item in self.orderitem.select_related():
            item.product.stock += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


# class OrderItemQuerySet(models.QuerySet):
#
#    def delete(self, *args, **kwargs):
#        for object in self:
#            object.product.stock += object.quantity
#            object.product.save()
#        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    # objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order,
                              related_name="orderitem",
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                verbose_name='product',
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity',
                                           default=0)

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

    # def delete(self):
    #     self.product.stock += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()






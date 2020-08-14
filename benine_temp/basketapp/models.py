from django.db import models
from django.conf import settings
from mainapp.models import Product
from pip.utils import cached_property

# class BasketQuerySet(models.QuerySet):
#
#    def delete(self, *args, **kwargs):
#        for object in self:
#            object.product.stock += object.quantity
#            object.product.save()
#        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Amount', default=0)
    add_datetime = models.DateTimeField(verbose_name='Time', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
    	return self.user.basket.select_related().all()

    # @property
    @cached_property
    def product_cost(self):

        return self.product.price * self.quantity

    @property
    # @cached_property
    def total_quantity(self):

        return sum(map(lambda x: x.quantity, self.get_items_cached))

    @property
    # @cached_property
    def total_cost(self):

        return sum(map(lambda x: x.product_cost, self.get_items_cached))

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)


    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.stock -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.stock -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
    #
    #
    # def delete(self):
    #     self.product.stock += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()



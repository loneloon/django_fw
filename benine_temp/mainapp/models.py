from django.db import models


class ProductCategory(models.Model):
    name = models.CharField('category name', max_length=64)
    description = models.TextField('category description', blank=True)


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, verbose_name='product category', on_delete=models.CASCADE)

    name = models.CharField('product name', max_length=64)
    tags = models.CharField('product tags', max_length=128, blank=True)
    description = models.TextField('product description', blank=True)
    image = models.ImageField('product image', upload_to='products_img', blank=True)
    price = models.DecimalField('product price', max_digits=8, decimal_places=2, null=True)
    discount = models.IntegerField('current discount', default=0)
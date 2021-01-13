# Generated by Django 2.2 on 2021-01-13 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='category name')),
                ('description', models.TextField(blank=True, verbose_name='category description')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='product name')),
                ('tags', models.CharField(blank=True, max_length=128, verbose_name='product tags')),
                ('level', models.IntegerField(blank=True, verbose_name='product level')),
                ('description', models.TextField(blank=True, verbose_name='product description')),
                ('image', models.ImageField(blank=True, upload_to='img/prods', verbose_name='product image')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True, verbose_name='product price')),
                ('discount', models.IntegerField(default=0, verbose_name='current discount')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('stock', models.IntegerField(default=0, verbose_name='stock')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProductCategory', verbose_name='product category')),
            ],
        ),
    ]

# Generated by Django 2.2 on 2020-07-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20200703_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='level',
            field=models.IntegerField(blank=True, verbose_name='product level'),
        ),
    ]

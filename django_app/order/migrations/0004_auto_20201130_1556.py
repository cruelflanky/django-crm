# Generated by Django 3.1.3 on 2020-11-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20201104_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='number_of_orders',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9, verbose_name='кол-во заказов'),
        ),
        migrations.AddField(
            model_name='shop',
            name='shop_token',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='токен магазина'),
        ),
    ]

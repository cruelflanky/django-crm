# Generated by Django 3.1.4 on 2021-01-06 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0036_auto_20210106_1938'),
        ('order', '0013_auto_20210106_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shop_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.shop', verbose_name='магазин'),
        ),
        migrations.DeleteModel(
            name='Shop',
        ),
    ]
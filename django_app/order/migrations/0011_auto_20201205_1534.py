# Generated by Django 3.1.3 on 2020-12-05 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20201204_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_secondname',
            field=models.CharField(default='-', max_length=50, null=True, verbose_name='отчество'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-05 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20201205_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_secondname',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='отчество'),
        ),
    ]

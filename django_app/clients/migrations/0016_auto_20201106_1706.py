# Generated by Django 3.0.7 on 2020-11-06 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0015_auto_20201106_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsstatus',
            name='name',
            field=models.CharField(max_length=250, verbose_name='услуга'),
        ),
    ]

# Generated by Django 3.1.4 on 2021-01-13 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_auto_20210106_1938'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='profile',
        ),
    ]

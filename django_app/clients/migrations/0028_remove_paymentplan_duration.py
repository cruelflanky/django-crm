# Generated by Django 3.1.3 on 2020-11-27 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0027_paymentplan_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentplan',
            name='duration',
        ),
    ]

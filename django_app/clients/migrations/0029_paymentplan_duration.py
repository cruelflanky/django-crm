# Generated by Django 3.1.3 on 2020-11-27 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0028_remove_paymentplan_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentplan',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(14)),
        ),
    ]

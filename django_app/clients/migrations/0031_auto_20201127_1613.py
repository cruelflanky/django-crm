# Generated by Django 3.1.3 on 2020-11-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0030_profile_payment_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='payment_end',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]

# Generated by Django 3.0.7 on 2020-11-06 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0014_smsstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smsstatus',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
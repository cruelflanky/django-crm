# Generated by Django 3.1.3 on 2020-11-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, default=None, max_length=50, null=True, verbose_name='Role'),
        ),
    ]

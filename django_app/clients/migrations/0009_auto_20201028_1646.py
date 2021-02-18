# Generated by Django 3.0.7 on 2020-10-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20201028_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='prom_id',
            field=models.CharField(default=None, max_length=50, verbose_name='Prom ID'),
        ),
        migrations.AddField(
            model_name='profile',
            name='prom_token',
            field=models.CharField(default=None, max_length=50, verbose_name='Prom token'),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegram_active',
            field=models.BooleanField(default=False, verbose_name='Telegram on/off'),
        ),
        migrations.AddField(
            model_name='profile',
            name='telegram_token',
            field=models.CharField(default=None, max_length=50, verbose_name='Telegram Token'),
        ),
        migrations.AddField(
            model_name='profile',
            name='viber_active',
            field=models.BooleanField(default=False, verbose_name='Viber on/off'),
        ),
        migrations.AddField(
            model_name='profile',
            name='viber_token',
            field=models.CharField(default=None, max_length=50, verbose_name='Viber Token'),
        ),
    ]

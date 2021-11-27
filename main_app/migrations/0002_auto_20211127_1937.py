# Generated by Django 3.2.6 on 2021-11-27 16:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='delivery',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='deliveries', to='main_app.Product', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='design',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 16, 37, 20, 186898, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 27, 16, 37, 20, 186898, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='production',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 4, 16, 37, 20, 186898, tzinfo=utc), verbose_name='Время окончания'),
        ),
    ]
# Generated by Django 3.2.6 on 2021-11-24 15:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20211124_1849'),
    ]

    operations = [
        migrations.AddField(
            model_name='design',
            name='type',
            field=models.CharField(choices=[('Компьютерное моделирование', 'Компьютерное моделирование'), ('Бумажное проектирование', 'Бумажное проектирование')], default='Компьютерное моделирование', max_length=40, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='design',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 15, 55, 14, 205259, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 24, 15, 55, 14, 203255, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AlterField(
            model_name='production',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 15, 55, 14, 205259, tzinfo=utc), verbose_name='Время окончания'),
        ),
    ]
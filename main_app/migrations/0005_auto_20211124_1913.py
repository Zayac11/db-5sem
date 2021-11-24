# Generated by Django 3.2.6 on 2021-11-24 16:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20211124_1858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='design',
            old_name='start_date',
            new_name='timestamp_start',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='start_date',
            new_name='timestamp_start',
        ),
        migrations.RenameField(
            model_name='production',
            old_name='start_date',
            new_name='timestamp_start',
        ),
        migrations.RemoveField(
            model_name='design',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='order',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='production',
            name='end_date',
        ),
        migrations.AddField(
            model_name='design',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 16, 13, 30, 898719, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AddField(
            model_name='order',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 24, 16, 13, 30, 896722, tzinfo=utc), verbose_name='Время окончания'),
        ),
        migrations.AddField(
            model_name='production',
            name='timestamp_end',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 1, 16, 13, 30, 899718, tzinfo=utc), verbose_name='Время окончания'),
        ),
    ]

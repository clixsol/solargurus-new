# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-07 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0019_package_price_per_kwh'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='turn_around_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

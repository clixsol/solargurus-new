# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-07-07 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0035_auto_20190707_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='impressions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='package',
            name='page_views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='package',
            name='phone_clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='package',
            name='website_clicks',
            field=models.IntegerField(default=0),
        ),
    ]

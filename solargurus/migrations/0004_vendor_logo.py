# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0003_auto_20170314_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='logo',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
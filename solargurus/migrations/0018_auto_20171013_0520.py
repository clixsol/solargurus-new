# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-13 05:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0017_auto_20171011_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='energyadvisor',
            name='password',
            field=models.CharField(default='password', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='realestateagent',
            name='password',
            field=models.CharField(default='password', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vendor',
            name='password',
            field=models.CharField(default='password', max_length=200),
            preserve_default=False,
        ),
    ]
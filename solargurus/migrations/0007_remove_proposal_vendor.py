# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 13:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0006_loi_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='vendor',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-08-18 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0039_auto_20190818_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enduser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]

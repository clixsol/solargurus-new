# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-25 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0021_package_ground_mounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='energyadvisor',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solargurus.Vendor'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-08 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0011_auto_20171008_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referralcode',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='referralcode',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-11-15 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0044_optcodesgenerated_otpcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optcodesgenerated',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='OTP Code'),
        ),
        migrations.AlterField(
            model_name='otpcode',
            name='code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='OTP Code'),
        ),
    ]

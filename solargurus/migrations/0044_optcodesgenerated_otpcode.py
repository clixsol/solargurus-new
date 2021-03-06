# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-11-15 09:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solargurus', '0043_auto_20190906_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptCodesGenerated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, max_length=4, null=True, verbose_name='OTP Code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Generated Opt Code',
                'verbose_name_plural': 'Generated Opt Codes',
            },
        ),
        migrations.CreateModel(
            name='OtpCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(blank=True, max_length=4, null=True, verbose_name='OTP Code')),
                ('is_activated', models.BooleanField(default=False, verbose_name='Is Activated')),
                ('activated_on', models.DateTimeField(blank=True, verbose_name='Activated on')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Opt Code',
                'verbose_name_plural': 'Opt Codes',
            },
        ),
    ]

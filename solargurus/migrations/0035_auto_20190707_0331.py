# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-07-07 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0034_vendor_certified'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeadTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('icon', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name': 'Lead Type',
                'verbose_name_plural': 'Lead Types',
            },
        ),
        migrations.AddField(
            model_name='loi',
            name='lead_source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='solargurus.LeadTypes'),
        ),
    ]

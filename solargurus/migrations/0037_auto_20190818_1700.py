# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-08-18 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solargurus', '0036_auto_20190707_0400'),
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=300)),
            ],
            options={
                'verbose_name': 'Association',
                'verbose_name_plural': 'Associations',
            },
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='associations',
        ),
        migrations.AddField(
            model_name='vendor',
            name='associations',
            field=models.ManyToManyField(to='solargurus.Association'),
        ),
    ]

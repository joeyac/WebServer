# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-15 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20170215_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='v_language',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='v_memory',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='v_status',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='v_time',
        ),
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(default='waiting', max_length=20),
        ),
    ]

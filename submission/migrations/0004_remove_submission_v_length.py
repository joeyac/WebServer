# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-14 00:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0003_auto_20170310_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='v_length',
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-06 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0007_problem_test_case_dir_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='hint',
            field=models.TextField(blank=True, default='', max_length=10000),
        ),
    ]

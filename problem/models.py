# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from submission.models import Submission
from utils.result import RESULT


OJ_NAME_CHOICE = (
    ('POJ', 'POJ'),
    ('HDU', 'HDU'),
    ('Codeforces', 'Codeforces'),
    ('USTBOJ', 'USTBOJ'),
)


class ProblemTag(models.Model):
    name = models.CharField(max_length=30)

    # because of query indeed cannot have space
    short_name = models.CharField(max_length=10)

    intro = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    problem_id = models.AutoField(primary_key=True, verbose_name='PID')
    virtual_id = models.CharField(max_length=50, verbose_name='VID')
    oj_name = models.CharField(max_length=50, choices=OJ_NAME_CHOICE, verbose_name='OJ')

    title = models.CharField(max_length=100, verbose_name='Title')
    source = models.CharField(max_length=255, blank=True, null=True, verbose_name='Source')

    # detail
    # time unit:ms
    time_limit = models.IntegerField(default=-1)
    # memory unit:kb
    memory_limit = models.IntegerField(default=-1)
    # os system:
    os = models.CharField(max_length=50)
    # description:
    description = models.TextField(max_length=30000, default="")
    input_description = models.TextField(max_length=10000, default="")
    output_description = models.TextField(max_length=10000, default="")
    input_sample = models.TextField(max_length=10000, default="")
    output_sample = models.TextField(max_length=10000, default="")

    hint = models.CharField(blank=True, default="", max_length=255)


    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField(ProblemTag, blank=True)

    visible = models.BooleanField(default=True)

    test_case_id = models.CharField(blank=True, null=True, max_length=20)


    remote_submission_user_number = models.IntegerField(default=-1)
    remote_accepted_user_number = models.IntegerField(default=-1)

    def __str__(self):
        return self.title

    def accepted_user_number(self):
        ac_count = Submission.objects.all().filter(problem=self, status=RESULT['accepted']).count()
        return ac_count

    def submission_user_number(self):
        count = Submission.objects.all().filter(problem=self).count()
        return count
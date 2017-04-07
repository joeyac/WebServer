# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Judger(models.Model):
    name = models.CharField(max_length=30)
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()

    max_judge_number = models.IntegerField(default=1)
    use_judge_number = models.IntegerField(default=0)

    token = models.CharField(max_length=65)

    active = models.BooleanField(default=True)

    status = models.CharField(max_length=31, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "judger"


class JudgeQueue(models.Model):
    # submission_id language_name src_code
    # judge: time_limit memory_limit test_case_id
    # # spj_code
    # vjudge: oj problem_id
    # global
    submission_id = models.IntegerField()
    language_name = models.CharField(max_length=30)
    src_code = models.TextField()

    # judge
    time_limit = models.IntegerField(default=-1)  # ms
    memory_limit = models.IntegerField(default=-1)  # kb
    test_case_id = models.CharField(blank=True, null=True, max_length=20)

    # spj_code
    spj_code = models.TextField(blank=True, null=True)

    # vjudge
    oj = models.SmallIntegerField(default=-1)
    problem_id = models.CharField(blank=True, null=True, max_length=50)

    # info
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "judge_queue"

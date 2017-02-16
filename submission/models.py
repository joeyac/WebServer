# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from utils.result import RESULT, languages, RE_RESULT, RE_languages


class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True, verbose_name='SID')
    user = models.OneToOneField(User)

    # avoid circular import
    # http://stackoverflow.com/questions/7684408/django-cannot-import-name-x
    problem = models.OneToOneField('problem.Problem')


    # base info
    # language = models.IntegerField(choices=list(RE_languages.items()))
    language = models.CharField(blank=True, null=True, max_length=50)

    code = models.TextField()
    shared = models.BooleanField(default=False)

    # status = models.IntegerField(default=RESULT['waiting'], choices=list(RE_RESULT.items()))
    status = models.CharField(default='waiting', max_length=20)

    time = models.IntegerField(blank=True, null=True)  # ms

    memory = models.IntegerField(blank=True, null=True)  # kb

    info = models.TextField(blank=True, null=True)
    ac_info = models.TextField(blank=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    judge_start_time = models.DateTimeField(blank=True, null=True)
    judge_end_time = models.DateTimeField(blank=True, null=True)

    # virtual judge info
    v_run_id = models.CharField(blank=True, null=True, max_length=100)
    # v_language = models.CharField(blank=True, null=True, max_length=50)
    v_length = models.CharField(blank=True, null=True, max_length=20)
    v_user = models.CharField(blank=True, null=True, max_length=50)
    v_submit_time = models.CharField(blank=True, null=True, max_length=50)
    # v_time = models.CharField(blank=True, null=True, max_length=30)
    # v_memory = models.CharField(blank=True, null=True, max_length=30)
    # v_status = models.CharField(blank=True, null=True, max_length=30)

    # contest

    @property
    def code_length(self):
        return len(self.code.encode('utf-8'))

    def __str__(self):
        return self.submission_id


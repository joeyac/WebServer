# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from judger.tasks import JudgeDispatcher


@shared_task
def p_judge(submission_id, language_name, src_code,
            time_limit=None, memory_limit=None,
            test_case_id=None, spj_code=None,
            oj=None, problem_id=None):

    JudgeDispatcher(submission_id, language_name, src_code,
                    time_limit, memory_limit,
                    test_case_id, spj_code,
                    oj, problem_id).judge()
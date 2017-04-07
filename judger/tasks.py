# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.db import transaction
from django.db.models import F
from django.utils.timezone import now
from judger.models import JudgeQueue, Judger
from submission.models import Submission
from judger.client import JudgeClient

from oj.settings import TEST_CASE_DIR
from utils.functions import zip_test_case

import json
import os

import logging
logger = logging.getLogger('app_info')


class JudgeDispatcher(object):
    # submission_id language_name src_code
    # judge: time_limit memory_limit test_case_id
    # # spj_code
    # vjudge: oj problem_id

    def __init__(self, submission_id, language_name, src_code,
                 time_limit=None, memory_limit=None, test_case_id=None, spj_code=None,
                 oj=None, problem_id=None):
        self.submission = Submission.objects.get(submission_id=submission_id)
        self.language_name = language_name
        self.src_code = src_code
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.test_case_id = test_case_id
        self.spj_code = spj_code
        self.oj = oj
        self.problem_id = problem_id

    @staticmethod
    def get_judger():
        with transaction.atomic():
            judgers = Judger.objects.select_for_update().filter(use_judge_number__lt=F("max_judge_number"),
                                                                active=True).order_by("max_judge_number")
            if judgers.exists():
                judger = judgers.first()
                judger.use_judge_number = F('use_judge_number') + 1
                judger.save()
                return judger

    @staticmethod
    def release_judger(judger_id):
        with transaction.atomic():
            judger = Judger.objects.select_for_update().get(id=judger_id)
            judger.use_judge_number = F('use_judge_number') - 1
            judger.save()

    def judge(self):
        judger = self.get_judger()
        self.submission.judge_start_time = now()

        if not judger:
            JudgeQueue.objects.create(submission_id=self.submission.submission_id, language_name=self.language_name,
                                      src_code=self.src_code, time_limit=self.time_limit,
                                      memory_limit=self.memory_limit, test_case_id=self.test_case_id,
                                      spj_code=self.spj_code, oj=self.oj, problem_id=self.problem_id)
            return
        try:
            client = JudgeClient(judger.token, 'http://{ip}:{port}'.format(ip=judger.ip_address, port=judger.port))
            if self.oj >= 1:  # vjudge
                res = client.vjudge(self.submission.submission_id, self.language_name, self.src_code, self.oj, self.problem_id)
                result = res['result']
                if res['code'] == 1:
                    self.submission.status = 'submit error'
                    self.submission.info = result['err']
                elif res['code'] == 2:
                    self.submission.status = 'judger error'
                    self.submission.info = result['data']
                elif res['code'] == 0:
                    result_map = ['v_run_id', 'v_submit_time', 'v_user', 'status', 'time', 'memory']
                    for item in result_map:
                        setattr(self.submission, item, result[item])

            else:  # local judge
                hash_sum = self.submission.problem.test_case_dir_hash
                remote_hash_sum = client.hash(self.submission.problem.test_case_id)
                print 1
                print hash_sum, remote_hash_sum
                print 2
                if str(hash_sum) != str(remote_hash_sum):
                    test_case_dir = os.path.join(TEST_CASE_DIR, self.submission.problem.test_case_id)
                    zip_file_path = zip_test_case(test_case_dir)
                    res = client.sync(self.submission.problem.test_case_id, zip_file_path)
                    print 'sync',
                    print res
                print 'start judge!'
                res = client.judge(self.submission.submission_id, self.language_name, self.src_code,
                                   self.time_limit, self.memory_limit, self.test_case_id)
                result = res['result']
                print res
                if res['code'] == 1:
                    self.submission.status = 'judger error'
                    self.submission.info = result['data']
                elif res['code'] == 2:
                    self.submission.status = 'unknown judger error'
                    self.submission.info = result['data']
                elif res['code'] == 0:
                    self.submission.status = result['status']
                    if result['status'] == 'accepted':
                        self.submission.time = result['time']
                        self.submission.memory = result['memory']
                    self.submission.info = json.dumps(result['info'])

        except Exception as e:
            logger.error(e)
            self.submission.status = 'system error'
            self.submission.info = str(e)
        finally:
            self.release_judger(judger.id)
            self.submission.judge_end_time = now()
            self.submission.save()

        with transaction.atomic():
            waiting_submissions = JudgeQueue.objects.select_for_update().all()
            if waiting_submissions.exists():
                from submission.tasks import p_judge
                waiting_submission = waiting_submissions.first()
                waiting_submission.delete()
                p_judge.delay(submission_id=waiting_submission.submission_id,
                              language_name=waiting_submission.language_name,
                              src_code=waiting_submission.src_code,
                              time_limit=waiting_submission.time_limit,
                              memory_limit=waiting_submission.memory_limit,
                              test_case_id=waiting_submission.test_case_id,
                              spj_code=waiting_submission.spj_code,
                              oj=waiting_submission.oj,
                              problem_id=waiting_submission.problem_id)


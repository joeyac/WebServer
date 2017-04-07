# coding=utf-8
from __future__ import unicode_literals
import hashlib
import requests


class JudgeClientError(Exception):
    pass


class JudgeClient(object):
    def __init__(self, token, server_base_url):
        self.token = hashlib.sha256(token).hexdigest()
        # 3c469e9d6c5875d37a43f353d4f88e61fcf812c66eee3457465a40b0da4153e0
        self.server_base_url = server_base_url.rstrip("/")

    def _request(self, url, data=None, files=None):
        headers = {"Authorization": 'Token ' + self.token}
        try:
            if files:
                return requests.post(url, headers=headers, data=data, files=files, timeout=30).json()
            elif data:
                print '------------'
                print url
                print self.token
                print data
                print '------------'
                return requests.post(url, headers=headers, json=data, timeout=30).json()
            else:
                return requests.get(url, headers=headers, timeout=30).json()
        except Exception as e:
            raise JudgeClientError(e.message)

    def ping(self):
        return self._request(self.server_base_url + '/ping/')

    def judge(self, submission_id, language_name, src_code, time_limit, memory_limit, test_case_id):
        data ={
            'submission_id': submission_id,
            'language_name': language_name,
            'src_code': src_code,

            'time_limit': time_limit,  # ms
            'memory_limit': memory_limit,  # kb
            'test_case_id': test_case_id,

        }
        return self._request(self.server_base_url + "/judge/", data=data)

    def hash(self, test_case_id):
        data = {
            'test_case_id': test_case_id,
        }
        return self._request(self.server_base_url + "/hash/", data=data)

    def sync(self, test_case_id, file_path):
        # TODO
        # 该方法只适用于上传小文件，上传大文件的时候就需要用到流式上传，否则占用主机内存太多。
        # 参考文档http://docs.python-requests.org/zh_CN/latest/user/advanced.html#advanced。
        data = {'test_case_id': test_case_id, }
        files = {'zipfile': open(file_path, 'rb')}
        return self._request(self.server_base_url + "/sync/", data=data, files=files)

    def vjudge(self, submission_id, language_name, src_code, oj, problem_id):
        data = {
            'submission_id': submission_id,
            'language_name': language_name,
            'src_code': src_code,

            'oj': oj,
            'problem_id': problem_id,
        }
        return self._request(self.server_base_url + '/vjudge/', data=data)
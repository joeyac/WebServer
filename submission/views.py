# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from submission.serializers import SubmitCodeSerializer, UpdateStatusSerializer, IDSerializer
from submission.models import Submission
from submission.tasks import p_judge
from submission.forms import QueryForm

from problem.models import Problem

from submission.tables import SubmissionTable, OrderSubmissionTable
from django_tables2 import RequestConfig

from judger.models import Judger

from utils.result import front_lang, oj_name_to_code, result_default_list, lang_map_all, highlight_map
from utils.functions import get_status_html

from oj.settings import SERVER_TOKEN

from itertools import chain
import json


class SubmitCodeAPIView(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = SubmitCodeSerializer(data=request.data)
        user = request.user if request.user.is_authenticated() else None
        if not user:
            return Response('you should login first!', status=status.HTTP_401_UNAUTHORIZED)
        check, second = user.profile.consume()
        if not check:
            info = 'You have submitted too fast.Please submit after about {time} second(s).'.format(time=second)
            return Response(info, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            data = serializer.data
            problem = Problem.objects.get(problem_id=data['problem_id'])
            language = data['lang']
            code = data['code']
            shared = data['shared']
            new_submission = Submission.objects.create(user=user, problem=problem,
                                                       code=code, shared=shared,
                                                       language=language)
            # # TODO: delete time sleep
            # import time
            # time.sleep(2)

            # submission_id, language_name, src_code,
            # time_limit=None, memory_limit=None, test_case_id=None, spj_code=None,
            # oj=None, problem_id=None
            sid = new_submission.submission_id
            lang_name = front_lang[problem.oj_name][language]
            if problem.oj_name == 'USTBOJ':
                time_limit = problem.time_limit
                memory_limit = problem.memory_limit
                test_case_id = problem.test_case_id
                p_judge.delay(submission_id=sid,language_name=lang_name, src_code=code,
                              time_limit=time_limit, memory_limit=memory_limit, test_case_id=test_case_id)
            else:
                oj_code = oj_name_to_code[problem.oj_name]
                problem_id = problem.virtual_id
                p_judge.delay(submission_id=sid, language_name=lang_name, src_code=code,
                              oj=oj_code, problem_id=problem_id)

            return Response('success!', status=status.HTTP_200_OK)
        else:
            key, value = serializer.errors.popitem()
            info = key + ':' + value[0] + '!'
            return Response(info, status=status.HTTP_400_BAD_REQUEST)


class SubmissionInfo(APIView):

    def post(self, request):
        user = request.user if request.user.is_authenticated() else None
        serializer = IDSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            result = []
            for id in data['ids']:
                submission = Submission.objects.get(submission_id=id)
                st = get_status_html(submission.status)
                memory = '—' if submission.memory is  None else submission.memory
                time = '—' if submission.time is None else submission.time

                res= {'id': id,
                      'status': st,
                      'memory': memory,
                      'time': time, }
                result.append(res)

            return Response(result, status=status.HTTP_200_OK)


# TODO 1. option orderable
# TODO 2. add language string in submission
# TODO 3. add html filter
# def submission_list(request):
#     user_name = request.user.username if request.user.is_authenticated() else None
#     submissions = Submission.objects.all()
#
#     run_id = request.GET.get('id')
#     submissions = submissions.filter(submission_id__lte=run_id) if run_id else submissions
#
#     user = request.GET.get('user')
#     submissions = submissions.filter(user__username=user) if user else submissions
#     print user
#
#     oj = request.GET.get('oj')
#     submissions = submissions.filter(problem__oj_name__iexact=oj) if oj else submissions
#
#     virtual_id = request.GET.get('vid')
#     submissions = submissions.filter(problem__virtual_id=virtual_id) if virtual_id else submissions
#
#     result = request.GET.get('status')
#     result = str(result).lower()
#     if result == 'all':
#         pass
#     elif result in result_default_list:
#         submissions = submissions.filter(status__icontains=result) if result else submissions
#
#     lang = request.GET.get('lang')
#     if lang and lang in front_lang['ALL']:
#         temp_submissions = {}
#         for key in lang_map_all:
#             new_submissions = submissions.filter(problem__oj_name__iexact=key, language__in=lang_map_all[key][lang])
#             temp_submissions = chain(temp_submissions, new_submissions)
#         submissions = temp_submissions
#
#     table = OrderSubmissionTable(submissions)
#     RequestConfig(request,  paginate={'per_page': 15}).configure(table)
#     data = {
#         'table': table,
#         'user': user_name,
#
#     }
#     return render(request, 'submission/submission_list.html', data)

def submission_list(request):
    user_name = request.user.username if request.user.is_authenticated() else None
    form = None
    submissions = Submission.objects.all()
    if request.method == 'POST':
        print request
        form = QueryForm(request.POST)
        if form.is_valid():
            query_username = form.cleaned_data['username']
            submissions = submissions.filter(user__username__iexact=query_username) if query_username else submissions

            pid = form.cleaned_data['pid']
            submissions = submissions.filter(problem__problem_id=pid) if pid else submissions

            result = form.cleaned_data['result']
            submissions = submissions.filter(status__icontains=result) if result else submissions

            lang = form.cleaned_data['lang']
            if lang:
                temp_submissions = {}
                for key in lang_map_all:
                    new_submissions = submissions.filter(problem__oj_name__iexact=key,
                                                         language__in=lang_map_all[key][lang])
                    temp_submissions = chain(temp_submissions, new_submissions)
                submissions = temp_submissions

            form = QueryForm(form.clean())

    if not form:
        form = QueryForm()

    table = OrderSubmissionTable(submissions)
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    data = {
        'table': table,
        'user': user_name,
        'form': form,
    }
    return render(request, 'submission/new_submission_list.html', data)


# TODO
def submission_detail(request, submission_id):
    user = request.user if request.user.is_authenticated() else None
    submission = Submission.objects.filter(submission_id=submission_id)
    table = SubmissionTable(submission)
    RequestConfig(request).configure(table)
    submission = Submission.objects.get(submission_id=submission_id)

    lang_name = front_lang[submission.problem.oj_name][submission.language]
    if lang_name in highlight_map:
        lang_name = highlight_map[lang_name]

    visible = True if user and (submission.user == user or submission.shared) else False
    src_code = submission.code

    test_case_info = None
    compile_info = None
    if submission.problem.oj_name == 'USTBOJ':
        if submission.status == 'compile error':
            compile_info = json.loads(submission.info, strict=False)
            compile_info = compile_info['data']

        out_of_list = ['compile error', 'system error', 'waiting', 'submit error', 'unknown error', ]
        if submission.status not in out_of_list:
            try:
                test_case_info = json.loads(submission.info, strict=False)
                info = []
                for item in test_case_info:
                    sub_status = get_status_html(item['status'])
                    temp_info = [int(item['info']['time']*1000), item['info']['max-rss'],
                                 sub_status, item['test_case']]
                    info.append(temp_info)
                test_case_info = info
            except:
                test_case_info = None
    else:
        compile_info = None

    data = {'table': table, 'visible': visible, 'submission': submission_id, 'lang_name': lang_name,
            'src_code': src_code, 'compile_info': compile_info, 'test_case_info': test_case_info}
    return render(request, 'submission/submission_list.html', data)


class UpdateStatusAPIView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = UpdateStatusSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            if data['token'] != SERVER_TOKEN:
                return Response('server token does not match.', status=status.HTTP_400_BAD_REQUEST)
            sid = data['submission_id']
            result = data['result']
            son = Submission.objects.get(submission_id=sid)
            son.status = result
            son.save()
            return Response(sid, status=status.HTTP_200_OK)

        else:
            key, value = serializer.errors.popitem()
            info = key + ':' + value[0] + '!'
            return Response(info, status=status.HTTP_400_BAD_REQUEST)

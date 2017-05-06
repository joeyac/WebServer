# -*- coding: utf-8 -*-
from django.conf.urls import url
from submission.views import SubmitCodeAPIView,UpdateStatusAPIView, submission_list, SubmissionInfo, submission_detail

urlpatterns = [
    url(r'^api/submission/update/$', UpdateStatusAPIView.as_view(), name='update_status'),

    url(r'^submit/problems/$', SubmitCodeAPIView.as_view(), name='submit_code'),
    url(r'^submissions/$', submission_list, name='submission_list'),

    url(r'^submission/(?P<submission_id>\d+)/$', submission_detail, name='submission_detail'),

    url(r'^submissions/get/$', SubmissionInfo.as_view(), name='get_submissions'),
]

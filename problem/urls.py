# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from problem.views import ProblemDataView, problem_list, problem_detail


urlpatterns = [
    url(r'^problems/(?P<tag_id>\d+)/$', problem_list, name='tag_problem_list'),
    url(r'^problems/$', problem_list, name='problem_list'),

    url(r'^problem/(?P<problem_id>\d+)/$', problem_detail, name='problem_detail'),

    url(r'^table/', include('table.urls')),
    url(r'^table/data/problems/$', ProblemDataView.as_view(), name='table_data_problem'),
]

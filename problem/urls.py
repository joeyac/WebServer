# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from problem.views import ProblemDataView, LocalProblemDataView,\
                        problem_list, local_problem_list,\
                        problem_detail


urlpatterns = [
    url(r'^problems/(?P<tag_id>\d+)/$', problem_list, name='tag_problem_list'),
    url(r'^problems/$', problem_list, name='problem_list'),

    url(r'^problems/local/(?P<tag_id>\d+)/$', local_problem_list, name='tag_local_problem_list'),
    url(r'^problems/local/$', local_problem_list, name='local_problem_list'),


    url(r'^problem/(?P<problem_id>\d+)/$', problem_detail, name='problem_detail'),

    url(r'^table/', include('table.urls')),
    url(r'^table/data/problems/$', ProblemDataView.as_view(), name='table_data_problem'),
    url(r'^table/data/problems/local$', LocalProblemDataView.as_view(), name='local_table_data_problem'),
]

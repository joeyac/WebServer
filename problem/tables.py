# -*- coding: utf-8 -*-
from problem.models import Problem
from submission.models import Submission

from table.columns import Column, DatetimeColumn, LinkColumn, Link
from table.tables import Table, TableDataMap
from table.utils import A

from django.core.urlresolvers import reverse_lazy
from django.utils.html import format_html, escape
import copy


class FlagColumn(Column):

    def __init__(self, user=None, **kwargs):
        self.user = user
        super(FlagColumn, self).__init__(**kwargs)

    def update(self, user):
        self.user = user

    def render(self, obj):
        if self.user:
            submissions = Submission.objects.filter(user=self.user, problem=obj)
            flag = 0  # None
            submit_cnt = 0
            submit_ac_cnt = 0
            if submissions:
                flag = 1
                submit_cnt = submissions.count()
                submissions = submissions.filter(status='accepted')
                if submissions:
                    submit_ac_cnt = submissions.count()
                    flag = 2
            if flag == 0:
                return ''
            elif flag == 2:
                info = 'Submit with {cnt} attempts, {ac_cnt} accepted.'.format(cnt=submit_cnt, ac_cnt=submit_ac_cnt)
                return format_html('&nbsp&nbsp<i class="fa fa-check" aria-hidden="true" '
                                   'data-toggle="tooltip" title="{info}" ></i>'.format(info=info))
            else:
                info = 'Submit with {cnt} attempts.'.format(cnt=submit_cnt)
                return format_html('&nbsp&nbsp<i class="fa fa-times" aria-hidden="true" '
                                   'data-toggle="tooltip" title="{info}" ></i>'.format(info=info))
        return ''


class PidColumn(Column):
    def render(self, obj):
        pid = A(self.field).resolve(obj)
        pid = str(pid)
        return pid.zfill(4)


class ProblemTable(Table):

    def __init__(self, user=None, **kwargs):
        ProblemTable.flag.update(user)
        self.base_columns[0] = self.flag
        del TableDataMap.map[self.token]
        TableDataMap.register(self.token, Problem, copy.deepcopy(self.base_columns))
        super(ProblemTable, self).__init__(**kwargs)

    # ('problem_id', 'oj_name', 'virtual_id', 'title', 'source', 'create_time')
    flag = FlagColumn(header=u'Flag', sortable=False, searchable=False, header_attrs={'width': '4%'})
    pid = PidColumn(field='problem_id', header=u'PID', searchable=False)
    oj_name = Column(field='oj_name', header=u'OJ')
    vid = Column(field='virtual_id', header=u'VID')
    # title = Column(field='title', header=u'Title')
    title = LinkColumn(field='title', header=u'Title',
                       links=[Link(text=A('title'), viewname='problem_detail', args=(A('problem_id'),))])

    source = Column(field='source', header=u'Source')
    create_time = DatetimeColumn(field='create_time', header=u'Create Time', header_attrs={'width': '20%'})

    class Meta:
        model = Problem
        attrs = {'class': 'table-hover table-striped table-condensed'}
        search = True
        search_placeholder = 'search'
        page_length = 25
        pagination = True
        ajax = True
        ajax_source = reverse_lazy('table_data_problem')


class LocalProblemTable(ProblemTable):
    class Meta:
        id = 'problemtable'
	model = Problem
        attrs = {'class': 'table-hover table-striped table-condensed'}
        search = True
        search_placeholder = 'search'
        page_length = 15
        pagination = True
        ajax = True
        ajax_source = reverse_lazy('local_table_data_problem')

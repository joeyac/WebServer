# -*- coding: utf-8 -*-
from problem.models import Problem

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
            import random
            flag = random.randint(0, 2)
            if flag == 0:
                return ''
            elif flag == 1:
                return format_html('&nbsp&nbsp<i class="fa fa-check" aria-hidden="true"></i>')
            else:
                return format_html('&nbsp&nbsp<i class="fa fa-times" aria-hidden="true"></i>')
        return ''


class PidColumn(Column):
    def render(self, obj):
        pid = A(self.field).resolve(obj)
        pid = int(pid)
        return pid + 1000


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
    create_time = DatetimeColumn(field='create_time', header=u'Create Time', header_attrs={'width': '18%'})


    class Meta:
        model = Problem
        attrs = {'class': 'table-hover table-striped table-condensed'}
        search = True
        search_placeholder = 'search'
        page_length = 25
        pagination = True
        ajax = True
        ajax_source = reverse_lazy('table_data_problem')
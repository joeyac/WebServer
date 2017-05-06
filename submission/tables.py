# -*- coding: utf-8 -*-
from submission.models import Submission
import django_tables2 as tables
from django.db.models import F
from django.db.models.functions import Length
from django.urls import reverse
from utils.result import front_lang
from utils.functions import get_status_html
from django.utils.html import format_html


class SubmissionTable(tables.Table):
    # 	RunID	Username  PID	oj vid result		Time	Memory	Language Length  submit Time
    submission_id = tables.Column(orderable=True)

    # pid = tables.Column(verbose_name='Pid', accessor='problem')

    problem = tables.Column()

    status = tables.Column()

    time = tables.Column(verbose_name='Time(ms)')
    memory = tables.Column(verbose_name='Memory(kb)')

    language = tables.Column()

    code_length = tables.Column(verbose_name='Length')

    class Meta:
        model = Submission
        orderable = False
        order_by = '-submission_id'
        attrs = {
            'class': "table table-hover table-striped table-bordered table-responsive no-footer",
            # ='class': "table table-hover table-striped basetable cf dataTable",
            'width':"100%",
            'role': 'grid',
        }
        fields = ('submission_id', 'user', 'problem', 'status', 'time',
                  'memory', 'language', 'code_length', 'create_time')

    def render_status(self, value, record):
        html = get_status_html(value)
        value = str(value).lower().title()
        url = reverse('submission_detail', args=(record.submission_id,))
        if value == 'Compile Error':
            return format_html('<span class="ce"><a href="{url}">{str}</a></span>'.format(url=url, str=value))
        return html

    def render_language(self, value, record):
        lang_name = front_lang[record.problem.oj_name][value]
        url = reverse('submission_detail', args=(record.submission_id,))
        return format_html('<a href="{url}">{value}</a>'.format(url=url, value=lang_name))

    # def render_pid(self, value, record):
    #     return value.problem_id

    def render_problem(self, value):
        url = reverse('problem_detail', args=(value.problem_id, ))
        return format_html('<a href="{url}">{value}</a>'.format(url=url, value=value.__str__()))

    def order_code_length(self, queryset, is_descending):
        queryset = queryset.annotate(
            length=Length('code')
        ).order_by(('-' if is_descending else '') + 'length')
        return queryset, True

    def order_submission_id(self, queryset, is_descending):
        queryset = queryset.annotate(
            id=F('submission_id')
        ).order_by('-id')
        return queryset, True


class OrderSubmissionTable(SubmissionTable):
    pid = tables.Column(orderable=False, accessor='problem', verbose_name='Pid')

    def render_pid(self, value):
        return value.problem_id

    user = tables.Column(orderable=False)
    problem = tables.Column(orderable=False)
    status = tables.Column(orderable=False)

    class Meta:
        model = Submission
        orderable = True
        order_by = '-submission_id'
        attrs = {
            'class': "table table-hover table-striped table-bordered table-responsive no-footer",
            # ='class': "table table-hover table-striped basetable cf dataTable",
            'width':"100%",
            'role': 'grid',
        }
        fields = ('submission_id', 'user', 'pid', 'problem', 'status', 'time',
                  'memory', 'language', 'code_length', 'create_time')




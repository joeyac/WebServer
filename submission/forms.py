# -*- coding: utf-8 -*-
from django import forms


lang_all = ['c', 'c++', 'java', 'pascal', 'python', 'c#', 'other']
lang_choice = [
    ('', 'All'),
    ('c', 'c'),
    ('c++', 'c++'),
    ('java', 'java'),
    ('pascal', 'pascal'),
    ('python', 'python'),
    ('c#', 'c#'),
    ('other', 'other'),
]
result_default_list = ['accepted', 'presentation error', 'wrong answer','time limit', 'memory limit', 'output limit','runtime error', 'compile error', 'unknown error', 'waiting']
result_choice = [
    ('', 'All'),
    ('Accepted', 'Accepted'),
    ('Presentation Error', 'Presentation Error'),
    ('Wrong Answer', 'Wrong Answer'),
    ('Time Limit', 'Time Limit'),
    ('Memory Limit', 'Memory Limit'),
    ('Output Limit', 'Output Limit'),
    ('Runtime Error', 'Runtime Error'),
    ('Compile Error', 'Compile Error'),
    ('Unknown Error', 'Unknown Error'),
    ('Waiting', 'Waiting'),
]


class QueryForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, label='Username:')
    pid = forms.IntegerField(required=False, min_value=1, label='PID:')
    result = forms.ChoiceField(choices=result_choice, required=False, label='Status:')
    lang = forms.ChoiceField(choices=lang_choice, required=False, label='Language:')


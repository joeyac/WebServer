# -*- coding: utf-8 -*-
from problem.tables import ProblemTable
from problem.models import Problem, ProblemTag

from utils.result import RESULT, languages

from table.views import FeedDataView

from django.shortcuts import render
from django.db.models import Q, Count

from functools import reduce



def problem_detail(request, problem_id):
    user = request.user if request.user.is_authenticated() else None
    problem = Problem.objects.get(problem_id=problem_id, visible=True)
    data = {
        'problem': problem,
        'result': RESULT,
        'languages': languages,
    }

    return render(request, 'problem/problem_detail.html', data)


def problem_list(request, tag_id=None):
    user = request.user if request.user.is_authenticated() else None
    tag = None
    if tag_id:
        tag = ProblemTag.objects.get(id=tag_id)

    # print(ProblemDataView.update_tag(tag=None))

    problems = ProblemTable(user=user, data=Problem.objects.all())

    tags = ProblemTag.objects.annotate(problem_number=Count("problem"))\
        .filter(problem_number__gt=0).order_by("-problem_number")

    return render(request, "problem/problem_list.html", {'problems': problems, 'tags': tags, 'tag': tag})


class ProblemDataView(FeedDataView):
    token = ProblemTable.token

    def __init__(self, **kwargs):
        super(ProblemDataView, self).__init__(**kwargs)

    def get_queryset(self, **kwargs):
        return super(ProblemDataView, self).get_queryset().filter(visible=True)

    def filter_queryset(self, queryset):
        def get_filter_arguments(filter_target):
            """
            Get `Q` object passed to `filter` function.
            """
            queries = []
            fields = [col.field for col in self.columns if col.searchable]
            value = filter_target
            if value[0] == '*':
                value = value[1:]
                queries.append(Q(**{"tags__short_name__icontains": value}))
                return reduce(lambda x, y: x | y, queries)

            for field in fields:
                if not field:
                    continue
                key = "__".join(field.split(".") + ["icontains"])
                value = filter_target
                queries.append(Q(**{key: value}))

            return reduce(lambda x, y: x | y, queries)

        filter_text = self.query_data["sSearch"]
        if filter_text:
            for target in filter_text.split():
                queryset = queryset.filter(get_filter_arguments(target))
        return queryset


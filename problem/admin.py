from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from problem.models import ProblemTag, Problem


class ProblemAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'problem_id', 'oj_name', 'virtual_id', 'title',
                    'source', 'create_time', )
    list_display_links = ('pk', 'problem_id',)
    search_fields = ('oj', 'title', 'problem_id')


class ProblemTagAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'name', 'create_time',)
    list_display_links = ('pk', 'name',)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemTag, ProblemTagAdmin)
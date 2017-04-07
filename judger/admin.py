from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from judger.models import JudgeQueue, Judger


class JudgerAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'port', 'max_judge_number', 'use_judge_number' , 'active')
    list_display_links = ('name',)


class JudgeQueueAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'language_name')
    list_display_links = ('submission_id',)


admin.site.register(Judger, JudgerAdmin)
admin.site.register(JudgeQueue, JudgeQueueAdmin)


from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from submission.models import Submission


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_id', 'problem', 'user', 'status', 'create_time',)
    list_display_links = ('submission_id',)


admin.site.register(Submission, SubmissionAdmin)


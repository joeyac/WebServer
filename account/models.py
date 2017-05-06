# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from oj.settings import TOKEN_BUCKET_DEFAULT_CAPACITY, TOKEN_BUCKET_FILL_RATE
from submission.models import Submission
from utils.result import RESULT


# after doing math, i choose the Extending User Model Using a One-To-One Link
# ref:https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#proxy
class Profile(models.Model):
    """
    User:
    Username, password and email are required. Other fields are optional.
    is_staff: admin
    is_active:
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # 级联删除

    nickname = models.CharField(max_length=30, blank=True, null=True)
    school = models.CharField(max_length=200, blank=True, null=True)
    # date_joined DataTimeField
    # last_login DataTimeField
    major = models.CharField(max_length=200, blank=True, null=True)
    # real profile
    # problems_status = JSONField(default={}) instead of Query
    # accepted_problem_number = models.IntegerField(default=0)
    # submission_number = models.IntegerField(default=0)

    submit_timestamp = models.DateTimeField(blank=True, null=True)
    token = models.IntegerField(blank=True, null=True)

    def consume(self, token=1):
        if not self.submit_timestamp:
            self.submit_timestamp = timezone.now()
            self.token = TOKEN_BUCKET_DEFAULT_CAPACITY
            self.token -= token
            self.save(update_fields=['submit_timestamp', 'token'])
            return True, ''
        else:
            now = timezone.now()
            expected_second = (now - self.submit_timestamp).total_seconds()
            expected_minute = long(expected_second / 60)
            buff = TOKEN_BUCKET_FILL_RATE * expected_minute
            self.token = min(self.token + long(buff), TOKEN_BUCKET_DEFAULT_CAPACITY)

            if self.token >= token:
                self.token -= token
                self.submit_timestamp = now
                self.save(update_fields=['submit_timestamp', 'token'])
                return True, ''

            return False, int(60-expected_second) + 1

    def __str__(self):
        return self.nickname

    def accepted_problem_number(self):
        # i think the value should come from submissions
        ac_count = Submission.objects.all().filter(user=self.user, status=RESULT['accepted']).count()
        return ac_count

    def submission_number(self):
        # the same as up
        count = Submission.objects.all().filter(user=self.user).count()
        return count


# to use the signals,
# Generally speaking, you will never have to call the Profile’s save method. Everything is done through the User model.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.nickname = instance.username
        profile.save(update_fields=['nickname'])


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()




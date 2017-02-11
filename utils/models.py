from __future__ import unicode_literals

from django.db import models
# http://stackoverflow.com/questions/2610088/can-djangos-auth-user-username-be-varchar75-how-could-that-be-done
from django.db.models.signals import class_prepared


def smaller_username(sender, *args, **kwargs):
    # You can't just do `if sender == django.contrib.auth.models.User`
    # because you would have to import the model
    # You have to test using __name__ and __module__
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        sender._meta.get_field("username").max_length = 20

class_prepared.connect(smaller_username)


class OJ(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10, unique=True)

    exist_problem_number = models.IntegerField(default=0)

    def update(self, number):
        self.exist_problem_number = number

    class Meta:
        db_table = 'OJ'

    def __str__(self):
        return self.name
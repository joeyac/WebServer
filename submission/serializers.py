# -*- coding: utf-8 -*-
from rest_framework import serializers
from submission.models import Submission


class MySerializer(serializers.Serializer):
    def create(self, validated_data):
        super(MySerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        super(MySerializer, self).update(instance, validated_data)


class SubmitCodeSerializer(MySerializer):
    shared = serializers.BooleanField()
    lang = serializers.IntegerField()
    problem_id = serializers.IntegerField()
    code = serializers.CharField(min_length=50)


class UpdateStatusSerializer(MySerializer):
    # 并不获取最终结果，在判题未结束时更新状态
    token = serializers.CharField(max_length=65)
    result = serializers.CharField(max_length=50)
    submission_id = serializers.IntegerField()


class IDSerializer(MySerializer):
    ids = serializers.ListField(child=serializers.IntegerField(min_value=0))


class ViewSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('submission_id', 'user', 'problem', 'language', 'status', 'time', 'memory', 'create_time')
        read_only_fields = ('submission_id', 'user', 'problem', 'language', 'status', 'time', 'memory', 'create_time')




# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')




class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, min_length=3)
    password = serializers.CharField(max_length=20, min_length=3)
    confirm_password = serializers.CharField(max_length=20, min_length=4)
    email = serializers.EmailField(max_length=254)
    nickname = serializers.CharField(max_length=30, required=False)
    school = serializers.CharField(max_length=200, required=False)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, min_length=3)
    password = serializers.CharField(max_length=20, min_length=3)


class UserModifySerializer(serializers.Serializer):
    password = serializers.CharField(max_length=20, min_length=3)
    new_password = serializers.CharField(max_length=20, min_length=3, required=False)
    confirm_password = serializers.CharField(max_length=20, min_length=3, required=False)
    nickname = serializers.CharField(max_length=30, required=False)
    school = serializers.CharField(max_length=200, required=False)
    email = serializers.EmailField(max_length=254)

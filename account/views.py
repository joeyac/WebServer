# -*- coding: utf-8 -*-
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserModifySerializer

from django.contrib import auth
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile

import time


class UserRegisterAPIView(APIView):
    def post(self, request):
        """
        用户注册json api接口
        ---
        request_serializer: UserRegisterSerializer
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            try:
                User.objects.get(username=data['username'])
                return Response('username exist!', status=status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                pass
            if data['password'] != data['confirm_password']:
                return Response('password does not match!', status=status.HTTP_406_NOT_ACCEPTABLE)
            try:
                User.objects.get(email=data['email'])
                return Response('email exist!', status=status.HTTP_406_NOT_ACCEPTABLE)
            except User.DoesNotExist:
                pass
            user = User.objects.create_user(username=data['username'],
                                            email=data['email'],
                                            password=data['password'])
            profile = Profile.objects.get(user=user)
            if 'nickname' in data:
                profile.nickname = data['nickname']
                profile.save(update_fields=['nickname'])
            if 'school' in data:
                profile.school = data['school']
                profile.save(update_fields=['school'])

            if 'major' in data:
                profile.major = data['major']
                profile.save(update_fields=['major'])

            return Response('success!', status=status.HTTP_200_OK)
        else:
            key, value = serializer.errors.popitem()
            info = key + ':' + value[0] + '!'
            return Response(info, status=status.HTTP_400_BAD_REQUEST)
            # captcha = Captcha(request)
            # if not captcha.check(data["captcha"]):
               # pass


class UserLoginAPIView(APIView):

    def post(self, request):
        """
        用户登录json api接口
        ---
        request_serializer: UserLoginSerializer
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = auth.authenticate(username=data["username"], password=data["password"])
            if user:
                auth.login(request, user)
                return Response('success!', status=status.HTTP_200_OK)
            else:
                return Response('password incorrect!', status=status.HTTP_401_UNAUTHORIZED)
        else:
            key, value = serializer.errors.popitem()
            info = key + ':' + value[0] + '!'
            return Response(info, status=status.HTTP_400_BAD_REQUEST)


class UserModifyAPIView(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        用户修改信息json api接口
        ---
        request_serializer: UserModifySerializer
        """
        serializer = UserModifySerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            user = request.user
            new_password = data.get('new_password') or ''
            confirm_password = data.get('confirm_password') or ''
            change_password = False
            if new_password or confirm_password:
                if new_password != confirm_password:
                    return Response('Retype password does not match!', status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    change_password = True
            if not user.check_password(data['password']):
                return Response('password incorrect!', status=status.HTTP_401_UNAUTHORIZED)
            if change_password:
                user.set_password(new_password)
                user.save(update_fields=['password'])
            if user.email != data['email']:
                user.email = data['email']
                user.save(update_fields=['email'])

            nick_name = data.get('nickname') or ''
            school = data.get('school') or ''
            major = data.get('major') or ''
            if user.profile.nickname != nick_name:
                user.profile.nickname = nick_name
                user.profile.save(update_fields=['nickname'])

            if user.profile.school != school:
                user.profile.school = school
                user.profile.save(update_fields=['school'])

            if user.profile.major != major:
                user.profile.major = major
                user.profile.save(update_fields=['major'])
            return Response('success!', status=status.HTTP_200_OK)
        else:
            key, value = serializer.errors.popitem()
            info = key + ':' + value[0] + '!'
            return Response(info, status=status.HTTP_400_BAD_REQUEST)


def logout(request):
    theme = request.session['theme'] if 'theme' in request.session else 'journal'
    auth.logout(request)
    request.session['theme'] = theme
    return redirect(reverse('homepage'))


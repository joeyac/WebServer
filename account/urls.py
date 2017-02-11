# -*- coding: utf-8 -*-
from django.conf.urls import url
from account.views import UserLoginAPIView, UserRegisterAPIView, UserModifyAPIView, logout

urlpatterns = [
    url(r'^register/$', UserRegisterAPIView.as_view(), name='register'),
    url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^modify/$', UserModifyAPIView.as_view(), name='modify'),
    # url(r'^set_password/$', views.set_password, name='set_password'),


]
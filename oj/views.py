# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.status import HTTP_200_OK,HTTP_500_INTERNAL_SERVER_ERROR

from .models import Theme

from datetime import datetime
from django.utils import timezone


def set_theme(request, theme_name):
    request.session['theme'] = theme_name
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def index_page(request):
    code = """
// 测试代码高亮
#include <stdio.h>
int main(int argc,char *args[])//主函数
{
    FILE * f_in=fopen(args[1],"r");//测试输入
    FILE * f_out=fopen(args[2],"r");//测试输出
    FILE * f_user=fopen(args[3],"r");//用户输出
    int ret=0;//返回值
    int T,n,a,b;
    fscanf(f_in,"%d",&T);//从输入中读取数据组数T
    while(T--)
    {
        fscanf(f_in,"%d",&n);
        fscanf(f_user,"%d%d",&a,&b);
        if(a+b!=n)
            ret = 1;//Wrong Answer
    }
    fclose(f_in);
    fclose(f_out);
    fclose(f_user);
    return ret;
}

"""
    value = u"C\u8bed\u8a00\u7a0b\u5e8f\u8bbe\u8ba1\u7ec3\u4e60\uff08\u56db\uff09"
    return render(request,"index.html",{'code': code,'value':value})


class TimeAPIView(APIView):

    def get(self, request):
        # time = datetime.now().isoformat()
        time = timezone.now().isoformat()
        return Response(time, status=HTTP_200_OK)
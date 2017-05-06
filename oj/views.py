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


def acm_team(request):
    return render(request, "team.html")


def page_not_found(request):
    error_id = '404'
    error_info = '好像找不到你要的页面啊<br>哥们你是不是点错了<br>'
    return render(request, "404.html", {'id': error_id, 'info': error_info})


def page_error(request):
    error_id = '500'
    error_info = '完蛋服务器内部出了点问题<br>哥们干得漂亮！<br>'
    return render(request, "500.html", {'id': error_id, 'info': error_info})


def permission_denied(request):
    error_id = '403'
    error_info = '这个页面拒绝了你的访问<br>╮(╯▽╰)╭<br>'
    return render(request, "403.html", {'id': error_id, 'info': error_info})


def index_page(request):
    c_code = """
#include <stdio.h>
int a,b;
int main() {
    while (scanf("%d%d",&a,&b)!=EOF) {
        printf("%d\\n",a+b);
    }
    return 0;
}
"""
    cpp_code = """
#include <iostream>
using namespace std;
int main()
{
    int a,b;
    while(cin>>a>>b){
        cout<<a+b<<endl;
    }
    return 0;
}
"""
    java_code = """
import java.util.*;
import java.io.*;
public class Main{
    static public void main(String[] args) throws IOException {
        Scanner cin =new Scanner(System.in);
        while(cin.hasNext()) {
            int a = cin.nextInt();
            int b = cin.nextInt();
            System.out.println(a + b);
        }
    }
}
"""
    py2_code = """
while True:
    try:
        a, b = map(int, raw_input().strip().split())
        print a + b
    except EOFError:
        break
"""
    py3_code = """
while True:
    try:
        a, b = map(int, input().strip().split())
        print (a + b)
    except EOFError:
        break
"""
    return render(request,"index.html",{'c_code': c_code,'cpp_code': cpp_code,
                                        'java_code': java_code,'py2_code': py2_code,
                                        'py3_code': py3_code, })


class TimeAPIView(APIView):

    def get(self, request):
        # time = datetime.now().isoformat()
        time = timezone.now().isoformat()
        return Response(time, status=HTTP_200_OK)
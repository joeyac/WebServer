"""oj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import index_page, set_theme, TimeAPIView, acm_team
from .views import page_error, page_not_found, permission_denied
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^summernote/', include('django_summernote.urls')),

    url(r'', include('account.urls')),
    url(r'', include('problem.urls')),
    url(r'', include('submission.urls')),

    url(r'^$', index_page, name='homepage'),
    url(r'^theme/(?P<theme_name>[\w-]+)/$', set_theme, name='set_theme'),
    url(r'^time/$', TimeAPIView.as_view(), name='server_time'),

    url(r'^acm_team/$', acm_team, name='acm_team'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += url(r'^no_page/$', permission_denied, name='no_page'),
    favicon_view = RedirectView.as_view(url='/static/img/favicon.ico', permanent=True)
    urlpatterns += [
        url(r'^favicon\.ico$', favicon_view),
    ]
else:
    handler403 = permission_denied
    handler404 = page_not_found
    handler500 = page_error
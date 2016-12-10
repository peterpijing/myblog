#coding=utf-8
"""blog_Project URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin

#1.定义图片文件上传路径
from django.conf import settings
import django

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/',include('blog.urls',namespace='blog')),

# # 1.定义图片文件上传路径
#     url(
#         r'^uploads/(?P<path>.*)$',\
#         django.views.static.serve, \
#         {'document_root':settings.MEDIA_ROOT,}
#         ),


    url(r'^sqlrelease/',include('sqlrelease.urls',namespace='sqlrelease')),

    url(r'^focus/',include('focus.urls',namespace='focus')),

    url(r'^keepblog/',include('keepblog.urls',namespace='keepblog')),
]

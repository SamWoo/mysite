"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.static import serve

from blog import views
from mysite.settings import STATIC_ROOT

app_name = 'blog'
urlpatterns = [
    # 首页
    url(r'^$', views.index, name='index'),
    # 博客详情页面
    url(r'^blog/(?P<pk>\d+)$', views.detail, name='detail'),
    # 归档页面
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    # 分类页面
    url(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    # 标签云页面
    url(r'^tag/(?P<pk>[0-9]+)/$', views.tag, name='tag'),
    # 关于我
    url(r'^about/$', views.about, name='about'),
    # search
    url(r'^search/$', views.search, name='search'),
    url(r'^blog-post/$', views.blog_post, name='blog_post'),
    url(r'^add-likes/$', views.add_likes, name='add_likes'),
    url(r'^ajax/$', views.testajax, name='ajax'),
    url(r'^modify/$', views.modify, name='modify'),
    # 添加静态文件的访问处理函数
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': STATIC_ROOT}),
]

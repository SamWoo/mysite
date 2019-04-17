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

import xadmin
from blog import views
from mysite.settings import STATIC_ROOT

urlpatterns = [
    # url(r'admin/', admin.site.urls),
    url(r'xadmin/', xadmin.site.urls),
    url(r'', include('blog.urls')),
    url(r'', include('comment.urls')),
    url(r'', include('user.urls')),
    url(r'', include('gallery.urls')),
    # 将 auth 应用中的 urls 模块包含进来
    url(r'', include('django.contrib.auth.urls')),
    url(r'mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# https://www.cnblogs.com/derek1184405959/p/8747961.html

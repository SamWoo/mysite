from django.conf.urls import url

from user import views

app_name = 'user'
urlpatterns = [
    url(r'register/$', views.register, name='register'),
    # url(r'accounts/profile', views.profile, name='profile'),
    url(r'profile/$', views.myself, name='profile'),
    url(r'my-image/$', views.my_image, name='my_image')
]

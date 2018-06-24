from django.conf.urls import url

from user import views

app_name = 'user'
urlpatterns = [
    url(r'register/', views.register, name='register'),
    url(r'accounts/profile', views.profile, name='profile'),
]

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from user.models import UserInfo, Profile


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['address', 'profession', 'aboutme', 'birthday', 'phone', 'nickname']


class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['img', ]


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', ]

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    img = models.TextField(blank=True)

    class Meta:
        verbose_name = "用户图像"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True, default='渔舟唱晚')
    address = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    aboutme = models.TextField(blank=True)
    birthday = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'user:{}'.format(self.user.username)

class Student(models.Model):
    name = models.CharField(max_length=100, blank=True)
    number = models.CharField(max_length=20, blank=True)
    sex = models.CharField(max_length=1, default='0')
    age = models.IntegerField(blank=True, default=18)
    zhuanye = models.CharField(max_length=100, blank=True)
    clas = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'student:{}'.format(self.name)

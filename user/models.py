from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    img = models.ImageField(blank=True, max_length=65535)

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

from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from user.models import Profile


class ProfileInline(admin.StackedInline):  # 将UserProfile加入到Admin的user表中
    model = Profile
    verbose_name = 'profile'


class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)  # 去掉在admin中的注册
admin.site.register(User, ProfileAdmin)  # 用userProfileAdmin注册user

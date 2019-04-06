from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from user.models import Profile, UserInfo


class ProfileInline(admin.StackedInline):  # 将UserProfile加入到Admin的user表中
    model = Profile
    verbose_name = '用户'


class ProfileAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'birthday', 'address', 'profession', 'aboutme']
    list_filter = ['profession', 'birthday']


admin.site.unregister(User)  # 去掉在admin中的注册
admin.site.register(User, ProfileAdmin)  # 用userProfileAdmin注册user
admin.site.register(UserInfo, UserInfoAdmin)

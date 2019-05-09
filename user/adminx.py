from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

import xadmin
from user.models import Profile, UserInfo,Student
from xadmin import views


class ProfileInline(object):  # 将UserProfile加入到Admin的user表中
    model = Profile
    verbose_name = '用户'


class ProfileAdmin(object):
    inlines = (ProfileInline,)


class UserInfoAdmin(object):
    list_display = ['user', 'phone', 'birthday', 'address', 'profession', 'aboutme']
    list_filter = ['profession', 'birthday']

class StudentAdmin(object):
    list_display = ['name', 'number', 'sex', 'age', 'zhuanye', 'clas']
    lis_filter = ['number', 'zhuanye']

# 创建xadmin的基本管理配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# 全局修改,固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '博客后台管理界面'
    # 修改footer
    site_footer = 'SamBrother'
    # 收起菜单
    menu_style = 'accordin'


xadmin.site.unregister(User)  # 去掉在admin中的注册
xadmin.site.register(User, ProfileAdmin)  # 用userProfileAdmin注册user
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(Student, StudentAdmin)
# 将基本配置管理与View绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 将title与footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)

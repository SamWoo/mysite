from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'
    # app名字后台显示中文
    verbose_name = "我的博客"

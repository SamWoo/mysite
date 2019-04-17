from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'comment'
    # app名字后台显示中文
    verbose_name = "Blog评论"

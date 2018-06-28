from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import Blog


class Comment(models.Model):
    article = models.ForeignKey(Blog, verbose_name='评论所属文章', on_delete=models.CASCADE)
    # user_name = models.CharField(verbose_name='评论者名字', max_length=100)
    user = models.ForeignKey(User, verbose_name='评论所属文章', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)

    def __str__(self):
        return self.user.username + ':' + self.content[:20]

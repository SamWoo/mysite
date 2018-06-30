from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from blog.models import Blog


class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class Comment(models.Model):
    article = models.ForeignKey(Blog, verbose_name='评论所属文章', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='评论所属文章', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)

    parent = models.ForeignKey('self', default=None, blank=True, null=True, verbose_name='引用', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = verbose_name = u'评论'
        app_label = string_with_title('comment', u'评论管理')

    def __unicode__(self):
        return self.article.title + '_' + str(self.pk)

    __str__ = __unicode__

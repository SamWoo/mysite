from django.contrib import admin

# Register your models here.
# blog
import xadmin
from comment import models


class CommentAdmin(object):
    list_display = ['article', 'user', 'parent', 'content', 'created_time']


xadmin.site.register(models.Comment, CommentAdmin)

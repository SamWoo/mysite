from django.contrib import admin

# Register your models here.
import xadmin
from blog import models
from blog.models import Category, Tag


# blog
class BlogAdmin(object):
    list_display = ['title', 'thumb_img', 'category', 'create_time', 'modify_time']


# category
class CategoryAdmin(object):
    list_display = ['name']


# tag
class TagAdmin(object):
    list_display = ['name']


# xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(models.Blog, BlogAdmin)

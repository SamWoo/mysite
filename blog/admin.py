from django.contrib import admin

# Register your models here.
from blog import models
from blog.models import Category, Tag


# blog
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumb_img', 'category', 'create_time', 'modify_time']


# category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


# tag
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


# admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(models.Blog, BlogAdmin)

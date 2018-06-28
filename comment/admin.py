from django.contrib import admin

# Register your models here.
# blog
from comment import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'content', 'created_time']


admin.site.register(models.Comment, CommentAdmin)

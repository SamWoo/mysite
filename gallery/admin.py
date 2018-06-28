from django.contrib import admin

# Register your models here.
# blog
from gallery import models


class UploadImgAdmin(admin.ModelAdmin):
    list_display = ['img']


admin.site.register(models.Image, UploadImgAdmin)

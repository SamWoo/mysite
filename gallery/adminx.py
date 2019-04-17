from django.contrib import admin

# Register your models here.
# blog
import xadmin
from gallery import models


class UploadImgAdmin(object):
    list_display = ['img']


xadmin.site.register(models.Image, UploadImgAdmin)

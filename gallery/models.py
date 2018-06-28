from django.db import models


# Create your models here.
class Image(models.Model):
    img = models.ImageField(upload_to='image')
    # desc = models.CharField(verbose_name='图片描述', max_length=100, blank=True)

# Generated by Django 2.0.6 on 2018-06-26 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload_image', '0002_remove_image_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(upload_to='image'),
        ),
    ]

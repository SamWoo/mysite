# Generated by Django 2.0.6 on 2019-04-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20190405_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(blank=True, default='/static/images/avatar.jpg', upload_to=''),
        ),
    ]

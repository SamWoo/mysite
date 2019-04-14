#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : forms.py
# @Software : PyCharm
from django import forms

from blog.models import Blog


class BlogPostForm(forms.ModelForm):
    '''博客发布表单'''

    class Meta:
        model = Blog
        fields = ['title', 'content', 'category']

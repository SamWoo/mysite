#!/usr/bin/env python
# -*-coding:utf-8-*-
from django.db.models import Count

from ..models import Blog, Category, Tag
from django import template

register = template.Library()


@register.simple_tag
def get_recent_blogs(num=5):
    '''
    最新文章模板
    :param num:
    :return:
    '''
    return Blog.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def get_archives():
    '''
    归档模板
    :return:
    '''
    return Blog.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    '''
    分类模板
    :return:
    '''
    return Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)


@register.simple_tag
def get_tags():
    '''
    标签云模板
    :return:
    '''
    return Tag.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)

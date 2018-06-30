#!/usr/bin/env python
# -*-coding:utf-8-*-
import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    return markdown.markdown(
        value,
        extensions=['markdown.extensions.fenced_code',  # 解析代码块
                    'markdown.extensions.codehilite',  # codehilite即为代码高亮准备
                    # 'markdown.extensions.table',    # 解析表格
                    # 'markdown.extensions.toc',    # 解析目录TOC
                    ],
        safe_mode=True,
        enable_attributes=False)

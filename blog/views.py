# -*-coding:utf-8-*-
import datetime

import markdown
import json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
from blog.models import Blog, Category, Tag
from comment.forms import BlogCommentForm
from gallery.models import Image


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    blog_list = Blog.objects.all().order_by('-id')  # 获取所有博客数据
    # 分页功能
    paginator = Paginator(blog_list, 9, request=request)  # 5为每页展示的博客数目
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    # print(blog_list)
    print(blogs)
    # 获取Gallery图片
    # images = Image.objects.all()[:5]

    context = {
        'blog_list': blogs,
        # 'images': images,
    }

    return render(request, 'blog/index.html', context=context)


def detail(request, pk):
    '''
    博客详情界面
    :param request:
    :param blog_id:
    :return:
    '''
    blog = get_object_or_404(Blog, pk=pk)
    # 记得在顶部引入 markdown 模块
    blog.content = markdown.markdown(blog.content,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    blog.increase_views()  # 点击率+1
    previous_blog = blog.get_previous()  # previous blog
    next_blog = blog.get_next()  # next blog

    # 评论
    comment_list = blog.comment_set.all()
    form = BlogCommentForm

    context = {'blog': blog,
               'previous_blog': previous_blog,
               'next_blog': next_blog,
               'comment_list': comment_list,
               'form': form,
               }
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    '''
    归档
    :param request:
    :param year:
    :param month:
    :return:
    '''
    blog_list = Blog.objects.filter(create_time__year=year,
                                    create_time__month=month
                                    ).order_by('-create_time')  # 获取所有数据
    # print(blog_list)

    paginator = Paginator(blog_list, 9, request=request)  # 5为每页展示的博客数目
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    # print(blog_list)

    return render(request, 'blog/index.html', context={'blog_list': blogs})


def category(request, pk):
    '''
    分类
    :param request:
    :param pk:
    :return:
    '''
    cate = get_object_or_404(Category, pk=pk)
    blog_list = Blog.objects.filter(category=cate).order_by('-create_time')
    # print(blog_list)

    paginator = Paginator(blog_list, 9, request=request)  # 5为每页展示的博客数目
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    # print(blog_list)

    return render(request, 'blog/index.html', context={'blog_list': blogs})


def tag(request, pk):
    '''
    分类
    :param request:
    :param pk:
    :return:
    '''
    tag = get_object_or_404(Tag, pk=pk)
    blog_list = Blog.objects.filter(tag=tag).order_by('-create_time')
    # print(blog_list)

    paginator = Paginator(blog_list, 9, request=request)  # 5为每页展示的博客数目
    page = request.GET.get('page', 1)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    # print(blog_list)

    return render(request, 'blog/index.html', context={'blog_list': blogs})


def about(request):
    '''
    关于界面
    :param request:
    :return:
    '''
    return render(request, 'blog/about.html')


def search(request):
    '''
    搜索页面
    :param request:
    :return:
    '''
    if 'keywords' in request.GET and request.GET['keywords']:
        keywords = request.GET['keywords']
        blog_list = Blog.objects.filter(Q(title__icontains=keywords) | Q(content__icontains=keywords))

        paginator = Paginator(blog_list, 9, request=request)  # 5为每页展示的博客数目
        page = request.GET.get('page', 1)
        try:
            blogs = paginator.page(page)
        except PageNotAnInteger:
            blogs = paginator.page(1)
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)

        context = {'blog_list': blogs,
                   'keywords': keywords}

        return render(request, 'blog/search.html', context=context)
    else:
        return HttpResponse('Please submit a search term.')


@csrf_exempt
def testajax(request):
    if request.method == "POST":
        if request.is_ajax():
            username = request.POST.get("username", "admin")
            comment = request.POST.get("comment", "default comment!")
            data = {'username': username, 'comment': comment}
            print(data)
            # 返回当前评论
            html = u"<li>\
                        <div class=\"vmaig-comment-content\">\
                        <a><h1>{}</h1></a>\
                        {}\
                        <p>{}</p>\
                        </div>\
                            </li>".format(
                username,
                comment,
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            # return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
            return HttpResponse(html)
    else:
        return render(request, "blog/ajax.html")

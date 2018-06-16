# -*-coding:utf-8-*-
import markdown
from django.shortcuts import render, get_object_or_404
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
from blog.models import Blog, Category, Tag


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

    return render(request, 'index.html', context={'blog_list': blogs})


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
    return render(request, 'detail.html', context={'blog': blog,
                                                        'previous_blog': previous_blog,
                                                        'next_blog': next_blog})


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

    return render(request, 'index.html', context={'blog_list': blogs})


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

    return render(request, 'index.html', context={'blog_list': blogs})


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

    return render(request, 'index.html', context={'blog_list': blogs})


def about(request):
    '''
    关于界面
    :param request:
    :return:
    '''
    return render(request, 'about.html')

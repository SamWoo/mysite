# -*-coding:utf-8-*-
import datetime
import json
import os
import random

import markdown
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
from blog.forms import BlogPostForm
from blog.models import Blog, Category, Tag
from comment.forms import BlogCommentForm
from gallery.models import Image
from user.models import Student


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

    # 获取Gallery图片用于首页图片显示
    images = Image.objects.all()
    if images:
        img_list = list({random.choice(images) for i in range(5)})
        print(img_list)
    else:
        img_list = None
    context = {
        'blog_list': blogs,
        'images': img_list,
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


@login_required(login_url='login')
@csrf_exempt
def blog_post(request):
    '''
    博客发布界面
    :param request:
    :return:
    '''
    if request.method == 'POST':
        blog_post_form = BlogPostForm(data=request.POST)
        if blog_post_form.is_valid():
            check_data = blog_post_form.cleaned_data
            try:
                new_blog = blog_post_form.save(commit=False)
                # print('Title:{}\nContent:{}\nCategory:{}'.format(new_blog.title, new_blog.content, new_blog.category))
                new_blog.save()
                tag = random.choice(Tag.objects.all())

                new_blog.tag.add(tag)
                new_blog.save()

                return HttpResponse("1")
            except Exception as e:
                print(e)
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        blog_post_form = BlogPostForm()
        context = {
            "blog_post_form": blog_post_form,
        }
        return render(request, 'blog/blog_post.html', context=context)


@csrf_exempt
def add_likes(request):
    print('Haahahah .....')
    print(request.POST)
    pk = request.POST.get('pk')
    print(pk)
    # num=request.POST.get('num',0)

    blog = get_object_or_404(Blog, pk=pk)
    blog.likes += 1
    blog.save()


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


@csrf_exempt
def modify(request):
    if request.method == "POST":
        print(request.POST)
        action = request.POST.get('action')
        num = request.POST.get('num')
        if action == '0':  # modify
            obj = Student.objects.get(number=num)

            data = {
                'num': obj.number,
                'name': obj.name,
                'sex': obj.sex,
                'age': obj.age,
                'zhuanye': obj.zhuanye,
                'clas': obj.clas,
            }

            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type='application/json')
        elif action == '1':  # delete
            Student.objects.filter(number=num).delete()
            data = {
                'status': 1,
            }
            return JsonResponse(data=data)
        elif action == '2':  # save
            name = request.POST.get('name')
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            zhuanye = request.POST.get('zhuanye')
            clas = request.POST.get('clas')
            Student.objects.filter(number=num).update(name=name, number=num, age=age, sex=sex, zhuanye=zhuanye,
                                                      clas=clas)

            data = {
                'status': 1,
            }
            return JsonResponse(data=data)
        elif action == '3':
            name = request.POST.get('name')
            sex = request.POST.get('sex')
            age = request.POST.get('age')
            zhuanye = request.POST.get('zhuanye')
            clas = request.POST.get('clas')
            obj = Student.objects.create(name=name, number=num, age=age, sex=sex, zhuanye=zhuanye,
                                         clas=clas)
            obj.save()
            data = {
                'status': 1,
            }
            return JsonResponse(data=data)
    else:
        students = Student.objects.all()
        context = {
            'lists': students,
        }
        return render(request, 'blog/ajax.html', context=context)

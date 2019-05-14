from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from user.forms import RegisterForm
from user.models import Profile, UserInfo


def register(request):
    # 从 get 或者 post 请求中获取 next 参数值
    # get 请求中，next 通过 url 传递，即 /?next=value
    # post 请求中，next 通过表单传递，即 <input type="hidden" name="next" value="{{ next }}"/>
    redirect_to = request.POST.get('next', request.GET.get('next', ''))

    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            user = form.save()
            Profile.objects.create(user=user)
            UserInfo.objects.create(user=user)
            # 自动登录
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            if redirect_to:
                # 跳转之前浏览页面
                return redirect(redirect_to)
            else:
                # 注册成功，跳转回首页
                return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'registration/register.html', context={'form': form,
                                                                  'next': redirect_to,
                                                                  })


def profile(requset):
    return redirect('/')


@login_required(login_url='/login/')
@csrf_exempt
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = Profile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        print(request.POST)
        action = request.POST.get('action')
        if action == '0':
            nickname = userinfo.nickname
            phone = userinfo.phone
            email = user.email
            address = userinfo.address
            career = userinfo.profession
            birthday = userinfo.birthday

            data = {
                'nickname': nickname,
                'phone': phone,
                'email': email,
                'address': address,
                'career': career,
                'birthday': birthday,
            }
            return JsonResponse(data=data)
        elif action == '1':
            nickname = request.POST.get('nickname')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            career = request.POST.get('career')
            birthday = request.POST.get('birthday')
            if all([nickname, phone, email, address, career, birthday]):
                UserInfo.objects.filter(user=user).update(nickname=nickname, phone=phone, address=address,
                                                          profession=career, birthday=birthday)
                User.objects.filter(username=request.user.username).update(email=email)
                data = {
                    'status': 0,
                }
            else:
                data = {
                    'status': 1,
                }
            return JsonResponse(data=data)

    else:
        context = {
            "user": user,
            "userprofile": userprofile,
            "userinfo": userinfo
        }
        # print('img-->{}'.format(userprofile.img))
        return render(request, 'user/myself.html', context=context)


@login_required(login_url='/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        profile = Profile.objects.get(user=request.user.id)
        profile.img = img
        # print('save img ===> {}'.format(userprofile.img))
        profile.save()
        return HttpResponse("1")
    else:
        return render(request, 'user/imagecrop.html')

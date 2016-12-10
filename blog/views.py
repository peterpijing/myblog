#coding=utf-8
from django.shortcuts import render,redirect,HttpResponse

# Create your views here.

import logging


from django.conf import settings

#1.定义view日志器
logger = logging.getLogger('blog.views')


def global_settings(request):
    return {
        'SITE_NAME':settings.SITE_NAME,
        'SITE_DESC':settings.SITE_DESC,
    }

# def index(request):
#     try:
#         file = open('sss.txt','r')
#     except Exception as e:
#         logger.error(e)
#     return render(request,'add.html',locals())

from models import *

#2.定义分页器
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

def index(request):
    try:
        category_list = Category.objects.all()[:5]
    except Exception as e:
        logger.error(e)

#定义分页器，有问题？？？
    article_list = Article.objects.all()
    paginator = Paginator(article_list,1)  # 实例化一个分页对象
    try:
        page = int(request.GET.get('page',1)) #获取页码
        article_list = paginator.page(page)  #获取某页对应的记录
    except (InvalidPage,EmptyPage,PageNotAnInteger):
        article_list = paginator.page(1)
    except Exception as e:
        logger.error(e)

    return render(request,'add.html',{'category_list':category_list})

# #1.引入forms表单中定义的表单
# from forms import RegForm
# from django.contrib.auth import login,logout,authenticate
# from django.contrib.auth.hasher import make_password

#
# #1.注册
# def do_reg(request):
#     try:
#         if request.method == 'POST':
#         # 1.实例化表单对象
#             regform = RegForm(request.POST)
#             if regform.is_valid():
#                 user = User.objects.create(username=regform.cleaned_data["username"],
#                                            email=regform.cleaned_data["email"],
#                                            )
#                 user.save()
#
#         #2. 登陆
#                 #指定默认的登陆验证
#                 user.backend = 'django.contrib.auth.backends.ModelBackend'
#                 login(request,user)
#                 return redirect(request.POST.get('sourc_url'))
#             else:
#                 return HttpResponse('error')
#         else:
#             regform = RegForm()
#
#     except Exception as e:
#         logger.error(e)
#
# #2.登陆
# def do_login(request):
#     try:
#         if request.method == 'POST':
#             login_form = LoginForm(request.POST)
#             if login_form.is_valid():
#                 username = login_form.cleaned_data["username"]
#                 password = login_form.cleaned_data["password"]
#                 user = authenticate(username=username,password=password)
#                 if user is not None:
#                     user.backend = 'django.contrib.auth.backends.ModelBackend'
#                     login(request, user)
#                 else:
#                     return HttpResponse('username or password wrong')
# #3.注销
# def do_logout(request):
#     try:
#         logout(request)
#     except Exception as e:
#         print e
#         logger.error(e)
#     # return redirect(request.META)

#2.通过django forms 自定义一个提交表单
from forms import AddForm

#3.配置django发送邮件
from django.core.mail import send_mail

def add(request):
    if request.method == 'POST':  # 当提交表单时
        form = AddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']

            # #3.发送
            # send_mail('Subject here', 'Here is the message.', '3087542600@qq.com',
            #           ['3087542600@qq.com'], fail_silently=False)

            return HttpResponse(str(int(a)+int(b)))
    else:  # 当正常访问时
        form = AddForm()
    return render(request, 'blog/index.html', {'form': form})



from forms import RemarkForm
#1.处理表单评论的业务逻辑
def remark(request):
    if request.method == 'POST':
        #1.实例化评论表单对象
        form = RemarkForm(request.POST)
        if form.is_valid():
            myremark = Remark()
            myremark.subject = form.cleaned_data['subject']
            myremark.mail = form.cleaned_data['mail']
            myremark.topic = form.cleaned_data['topic']
            myremark.message = form.cleaned_data['message']
            myremark.cc_myself = form.cleaned_data['cc_myself']
            myremark.save()

    else:
        form = RemarkForm()
    ctx = {
        'form': form,
        'ties': Remark.objects.all()
    }
    return render(request, 'blog/message.html', ctx)


from forms import NormalUserForm
#2.定义图片上传处理逻辑
def registerNormalUser(request):
    if request.method == "POST":
        uf = NormalUserForm(request.POST,request.FILES)
        if uf.is_valid():
            # get the info of the form
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            # write in database
            normalUser = NormalUser()
            normalUser.username = username
            normalUser.headImg = headImg
            normalUser.save()
            return HttpResponse('Upload Succeed!')
    else:
        uf = NormalUserForm()
    return render(request,'blog/register.html',{'uf':uf})
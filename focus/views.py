#coding=utf-8
from django.shortcuts import render

# Create your views here.

from models import Article
from forms import LoginForm

#1.focus初始化页面
def index(request):
    latest_article_list = Article.objects.query_by_time()
    loginform = LoginForm()
    context = {'latest_article_list': latest_article_list, 'loginform': loginform}
    return render(request, 'focus/index.html', context)


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404

#2.登陆表单页面--验证(依赖于loginfrom表单)
def log_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'focus/login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['uid']
            password = form.cleaned_data['pwd']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #2.登陆成功后跳转到/focus页面
                url = request.POST.get('source_url', '/focus')
                return redirect(url)
            else:
                #2.登陆验证不成功，在当前页面返回错误
                return render(request, 'focus/login.html', {'form': form, 'error': "password or username is not ture!"})

        else:
            return render(request, 'focus/login.html', {'form': form})


#3用户注销页面
from django.contrib.auth.decorators import login_required
@login_required
def log_out(request):

	url = request.POST.get('source_url', '/focus/')
	logout(request)
	return redirect(url)

import  markdown2
from forms import CommmentForm
#4.文章页面
def article(request,article_id):
    article = get_object_or_404(Article,id=article_id)
    content = markdown2.markdown(article.content, extras=["code-friendly",
                                                          "fenced-code-blocks", "header-ids", "toc", "metadata"])
    commentform = CommmentForm()
    loginform = LoginForm()
    comments = '11'
    return render(request, 'focus/article_page.html', {
        'article': article,
        'loginform': loginform,
        'commentform': commentform,
        'content': content,
        'comments': comments
    })


import urlparse  #解析url
from models import Comment
#5.评论提交
@login_required
def comment(request, article_id):
	form  = CommmentForm(request.POST)
	url = urlparse.urljoin('/focus/', article_id)

	if form.is_valid():
		user = request.user
		article = Article.objects.get(id=article_id)
		new_comment = form.cleaned_data['comment']
		c = Comment(content=new_comment, article_id=article_id)  # have tested by shell
		c.user = user
		c.save()
		article.comment_num += 1
        print article.comment_num
	return redirect(url)


#6.浏览者favorites
@login_required
def get_keep(request, article_id):
    logged_user = request.user
    article = Article.objects.get(id=article_id)
    #???????? 这是查询什么的？？？
    articles = logged_user.article_set.all()
    if article not in articles:
        #6.没有和User表做关联，所以无论用户谁，都会增加一个收藏
        # article.user.add(logged_user)  # for m2m linking, have tested by shell
        article.keep_num += 1
        article.save()
        return redirect('/focus/')
    else:
        url = urlparse.urljoin('/focus/', article_id)
        return redirect(url)

from models import Poll
#7.投票
@login_required
def get_poll_article(request,article_id):
	logged_user = request.user
	article = Article.objects.get(id=article_id)
	polls = logged_user.poll_set.all()
	articles = []
	for poll in polls:
		articles.append(poll.article)

	if article in articles:
		url = urlparse.urljoin('/focus/', article_id)
		return redirect(url)
	else:
		article.poll_num += 1
		article.save()
		poll = Poll(user=logged_user, article=article)
		poll.save()
		data = {}
		return redirect('/focus/')


#8.新增文章表单
from forms import ArticleForm
from models import Article
from django.shortcuts import HttpResponse
@login_required
def addarticle(request):
    #8.实例化文章表单对象
    article = ArticleForm(request.POST)
    if article.is_valid():
        myarticle = Article()
        myarticle.title = article.cleaned_data['title']
        myarticle.content = article.cleaned_data['content']
        # myarticle.pub_date = article.cleaned_data['pub_date']
        # myarticle.update_time = article.cleaned_data['update_time']
        # myarticle.published = article.cleaned_data['published']
        # myarticle.poll_num = article.cleaned_data['poll_num']
        # myarticle.comment_num = article.cleaned_data['comment_num']
        # myarticle.keep_num = article.cleaned_data['keep_num']
        myarticle.author_id  = article.cleaned_data['author']
        myarticle.save()
        return HttpResponse('add ok')
    else:
        article = ArticleForm()
    return render(request, 'focus/add.html', {'article': article})


from forms import ChangepwdForm
#9.用户修改密码
@login_required
def changepwd(request):
    if request.method == 'GET':
        form = ChangepwdForm()
        return render(request,'focus/changepwd.html',{'form':form})
    else:
        form = ChangepwdForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = request.POST.get('newpassword1', '')
                user.set_password(newpassword)
                user.save()
                url = request.POST.get('source_url', '/focus')
                return redirect(url)
            else:
                return  render(request, 'focus/changepwd.html',{'form': form, 'error': "password  is not same!"})

        else:
            return render(request,'focus/changepwd.html',{'form': form})


from forms import RegisterForm
from models import NewUser
from django.core.exceptions import ObjectDoesNotExist
#10.用户注册(注册到了newuser表中了，并不是user表中？？？)无法被验证 login TODO
def register(request):
    error1 = "this name is already exist"
    valid = "this name is valid"

    if request.method == 'GET':
        form = RegisterForm()
        return render(request,'focus/register.html',{'form':form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if request.POST.get('raw_username', 'erjgiqfv240hqp5668ej23foi') != 'erjgiqfv240hqp5668ej23foi':
            try:
                user = NewUser.objects.get(username=request.POST.get('raw_username', ''))
            except ObjectDoesNotExist:
                return render(request, 'focus/register.html', {'form': form, 'msg': valid})
            else:
                return render(request, 'focus/register.html', {'form': form, 'msg': error1})

        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password1 = form.cleaned_data['password1']
                password2 = form.cleaned_data['password2']
                if password1 != password2:
                    return render(request, 'focus/register.html', {'form': form, 'msg': "two password is not equal"})
                else:
                    user = NewUser(username=username, email=email, password=password1)
                    user.save()
                    # return render(request, 'login.html', {'success': "you have successfully registered!"})
                    return redirect('/focus/login')
            else:
                return render(request, 'focus/register.html', {'form': form})






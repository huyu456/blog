from django.shortcuts import render, redirect
from .forms import LoginForm, RegForm
from django.contrib import auth
from django.urls import reverse
from blog.models import ReadNum, Blog, BlogType
from django.contrib.auth.models import User
import random


def rand_blogs(except_id=0):
    rand_count = 4
    return Blog.objects.exclude(id=except_id).order_by('?')[:rand_count]  # order_by('?')对应 order by random()


# 通过
def home(request):
    blogs = Blog.objects.all()
    hot_blog = ReadNum.objects.all().order_by('-read_num')

    context = {}
    context['blogs'] = blogs[:6]
    context['hot_blog'] = hot_blog[:6]
    context['random_blog'] = rand_blogs()
    context['blog_types'] = BlogType.objects.all()
    return render(request, 'home.html', context)


def Login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user=user)
            return redirect(request.GET.get('form', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form

    return render(request, 'login.html', context)


def Register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)

        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password']
            email = reg_form.cleaned_data['email']

            user = User.objects.create_user(username, password, email)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('form', reverse('home')))

    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form

    return render(request, 'register.html', context)


def Loginout(request):
    auth.logout(request)
    return redirect(request.GET.get('form', reverse('home')))

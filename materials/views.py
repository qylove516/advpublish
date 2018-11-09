from django.shortcuts import render, HttpResponse, redirect
from materials import models
from django.contrib.auth.models import auth
import json
import os, datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from materials import forms
from advpublish import settings
from collections import OrderedDict


def register(request):
    if request.method == 'POST':
        ret = {
            "status": 0,
            "msg": ""
        }
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():
            # 把确认密码去除
            form_obj.cleaned_data.pop("re_password")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data)
            ret["msg"] = "/login/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)
    form_obj = forms.RegForm()
    return render(request, 'register.html', {"form_obj": form_obj})


# 校验用户名是否已被注册
def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        ret["status"] = 1
        ret["msg"] = "用户名已被注册！"
    return JsonResponse(ret)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        ret = {"status": 0, "msg": ""}
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            ret["msg"] = ""
        else:
            ret["status"] = 1
            ret["msg"] = "用户名或密码错误！"
        return HttpResponse(json.dumps(ret))
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required
def index(request):
    return render(request, 'index.html')


def upload(request, tag):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}
        img = request.FILES.get("img")
        if not img:
            ret["msg"] = "上传文件为空，请重新选择文件！"
            return HttpResponse(json.dumps(ret))
        tag = request.POST.get("tag")
        tag = models.Tag.objects.filter(title=tag).first()
        title = img.name
        models.Material.objects.create(title=title, tag=tag, image=img, user=request.user)
        return HttpResponse(json.dumps(ret))
    select = models.Tag.objects.all()
    select = {
        "select": select
    }
    return render(request, "show_admin/upload_img.html", select)


def delete(request, tag):
    all_img = request.GET.get("all")
    all_img = json.loads(all_img)
    nid = request.GET.get("nid")
    ret = {"status": True}
    if nid:
        nid = json.loads(nid)
    if all_img:
        if request.user.is_superuser:
            try:
                models.Material.objects.all().delete()
            except Exception as e:
                ret["status"] = False
        else:
            try:
                models.Material.objects.filter(user=request.user).delete()
            except Exception as e:
                ret["status"] = False
    else:
        try:
            models.Material.objects.filter(nid=nid).delete()
        except Exception as e:
            ret["status"] = False
    return JsonResponse(ret)


def welcome(request):
    return render(request, 'home.html')


def material(request):
    tags = models.Tag.objects.all()
    materials = []
    if request.user.is_superuser:
        for tag in tags:
            file = models.Material.objects.filter(tag=tag).order_by("-create_time")
            materials.append(file)
    else:
        for tag in tags:
            file = models.Material.objects.filter(tag=tag, user=request.user).order_by("-create_time")
            materials.append(file)

    ret = {
        "tags": tags,
        "materials": materials
    }
    return render(request, 'material.html', ret)


def programme(request):
    return render(request, 'programme.html')


def user(request):
    return render(request, 'show_admin/user.html', {"name": "admin"})

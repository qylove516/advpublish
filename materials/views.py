from django.db.models import Count
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from advpublish import settings


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
    tags = models.FileTag.objects.all()
    users = models.UserInfo.objects.all()

    ret = {
        "tags": tags,
        "users": users
    }
    return render(request, 'index.html', ret)


def welcome(request):
    return render(request, 'home.html')


def materials(request):
    if request.user.is_superuser:
        file_list = models.MaterialFiles.objects.all().order_by("-create_time")
    else:
        file_list = models.MaterialFiles.objects.filter(user=request.user).order_by("-create_time")
    paginator = Paginator(file_list, 20)
    page = request.GET.get('page')
    try:
        current_page = paginator.page(page)
        files = current_page.object_list
    except PageNotAnInteger:
        current_page = paginator.page(1)
        files = current_page.object_list
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        files = current_page.object_list

    ret = {
        "pages": current_page,
        "files": files
    }
    return render(request, 'materials.html', ret)


def materials_add(request):
    file_types = settings.FILE_TYPES
    if request.method == 'POST':
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_obj = request.FILES.get('file')
        tag = request.POST.get('tag')
        title = file_obj.name
        ret = {"status": True, "msg": ""}
        if title.split(".")[-1] in file_types:
            file_path = os.path.join(settings.MEDIA_ROOT, "uploads", time + file_obj.name)
            try:
                f = open(file_path, "wb")
                for chunk in file_obj.chunks():
                    f.write(chunk)
                f.close()
                tag = models.FileTag.objects.filter(title=tag).first()
                tag_user = tag.user
                models.MaterialFiles.objects.create(title=title, tag=tag, files=file_path, user=tag_user)
                ret["msg"] = "上传成功！"
            except Exception as e:
                ret["status"] = False
                ret["msg"] = "上传失败"
        else:
            ret["status"] = False
            ret["msg"] = "不支持此文件格式！"
        return JsonResponse(ret)
    if request.user.is_superuser:
        tags = models.FileTag.objects.all()
    else:
        tags = models.FileTag.objects.filter(user=request.user)
    ret = {
        "tags": tags
    }
    return render(request, 'show_admin/materials_add.html', ret)


def materials_delete(request):
    pk = request.GET.get("pk")
    ret = {"status": True}
    if pk:
        pk = json.loads(pk)
        try:
            models.MaterialFiles.objects.filter(pk=pk).delete()
        except Exception as e:
            ret["status"] = False
    return JsonResponse(ret)


def tags(request):
    if request.method == "POST":
        title = request.POST.get("title")
        nid = request.POST.get("nid")
        ret = {"status": True, "msg": ""}
        try:
            tag = models.FileTag.objects.filter(nid=nid).first()
            tag.title = title
            tag.save()
            ret["msg"] = "更新成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "更新失败"
        return JsonResponse(ret)

    if request.user.is_superuser:
        tags = models.FileTag.objects.all()
        # num_count = models.FileTag.objects.annotate(num_article=Count("materialfiles")).values("materialfiles__title")
    else:
        tags = models.FileTag.objects.filter(user=request.user)
    ret = {
        "tags": tags,
    }
    return render(request, "tags.html", ret)


def tag_add(request):
    if request.method == 'POST':
        title = request.POST.get("title")
        user = request.user
        ret = {"status": True, "msg": ""}
        try:
            models.FileTag.objects.create(title=title, user=user)
        except Exception as e:
            ret["msg"] = "添加标签失败！"
        return JsonResponse(ret)

    if request.user.is_superuser:
        tags = models.FileTag.objects.all()
    else:
        tags = models.FileTag.objects.filter(user=request.user)
    ret = {
        "tags": tags
    }
    return render(request, 'show_admin/tags_add.html', ret)


def tags_update(request, pk):
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": ""}
        try:
            models.FileTag.objects.filter(pk=pk).update(title=title)
        except Exception as e:
            ret["msg"] = "修改失败！"
            ret["status"] = False
        return JsonResponse(ret)
    ret = {
        'pk': pk,
        'tag': models.FileTag.objects.filter(pk=pk).first()
    }
    return render(request, 'show_admin/tags_update.html', ret)


def tags_delete(request):
    if request.method == "GET":
        pk = request.GET.get("pk")
        ret = {"status": True, "msg": "删除成功！"}
        try:
            models.FileTag.objects.filter(pk=pk).delete()
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "删除失败！"
        return JsonResponse(ret)


def user(request):
    return render(request, 'show_admin/user.html')

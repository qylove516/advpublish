from django.db.models import Count, Q
from django.shortcuts import render, HttpResponse, redirect
from materials import models
from django.contrib.auth.models import auth
import json
import os, datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from materials import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from advpublish import settings
from materials.get_pgs import get_pg


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
    """
    判断用户的身份，超级用户与普通管理员返回的结果不同
    :param request:
    :return:
    """
    user = request.user
    area_interval = None
    users = None
    if user.is_superuser:
        users = models.UserInfo.objects.all().filter(~Q(is_superuser=True)).order_by("username")
        areas = models.Area.objects.all().order_by("-title")
        group = models.Group.objects.all().order_by("name")
    elif user.is_manage:
        group = user.groups.all().order_by("name")[0]
        users = group.user_set.all().order_by("-create_time")
        areas = group.area_set.all().order_by("group_id")
    else:
        group = user.groups.all().order_by("name")
        areas = []
        for g in group:
            for u in g.area_set.all().order_by("group_id"):
                areas.append(u)

    ret = {
        "area_interval": area_interval,
        "group": group,
        "users": users,
        "areas": areas
    }
    return render(request, 'index.html', ret)


def welcome(request):
    return render(request, 'home.html')


def materials(request):
    if request.user.is_superuser:
        files_all = models.MaterialFiles.objects.all().order_by("-create_time")
    else:
        files_all = models.MaterialFiles.objects.filter(user=request.user).order_by("-create_time")
    files, current_page = get_pg(request, files_all, 10)
    ret = {
        "files_all": files_all,
        "pages": current_page,
        "files": files
    }
    return render(request, 'materials.html', ret)


def materials_add(request):
    file_types = settings.FILE_TYPES
    if request.method == 'POST':
        time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_obj = request.FILES.get('file')
        tag_pk = request.POST.get('tag_pk')
        title = file_obj.name
        ret = {"status": True, "msg": ""}
        if title.split(".")[-1] in file_types:
            file_path = os.path.join(settings.MEDIA_ROOT, "uploads", time + file_obj.name)
            try:
                f = open(file_path, "wb")
                for chunk in file_obj.chunks():
                    f.write(chunk)
                f.close()
                tag = models.FileTag.objects.filter(pk=tag_pk).first()
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
    user = request.user
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

    if user.is_superuser:
        tags_all = models.FileTag.objects.all().order_by("user_id")
        # num_count = models.FileTag.objects.annotate(num_article=Count("materialfiles")).values("materialfiles__title")
    elif user.is_manage:
        group = user.groups.all()[0]
        users = group.user_set.all()
        tags_all = models.FileTag.objects.filter(user__in=users).order_by("user_id")
    else:
        tags_all = models.FileTag.objects.filter(user=user).order_by("user_id")
    tags, current_page = get_pg(request, tags_all, 8)
    ret = {
        "tags_all": tags_all,
        "tags": tags,
        "current_page": current_page
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
            tag = models.FileTag.objects.filter(pk=pk).first()
            tag.materialfiles_set.all().delete()
            tag.delete()
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "删除失败！"
        return JsonResponse(ret)


def user(request):
    return render(request, 'show_admin/user.html')

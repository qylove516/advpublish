from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from materials.get_pgs import get_pg


def adv_programme(request):
    # 普通用户在区域列表中查看是否已通过审请
    user = request.user
    if user.is_superuser:
        programmes = models.AdvProgramme.objects.all().filter()
    elif user.is_manage:
        group = user.groups.all()[0]
        users = group.user_set.all()
        programmes = []
        for user in users:
            for p in models.AdvProgramme.objects.all().filter(user=user):
                programmes.append(p)
    else:
        programmes = models.AdvProgramme.objects.filter(user=user)
    ret = {
        "programmes": programmes,
    }
    return render(request, 'programme.html', ret)


def adv_programme_add(request):
    if request.method == "POST":
        ret = {"status": True, "msg": ""}
        title = request.POST.get("title")
        try:
            if title:
                models.AdvProgramme.objects.create(title=title, user=request.user)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "新建节目单失败！"
        return JsonResponse(ret)
    return render(request, 'show_admin/programme_add.html')


def adv_programme_del(request):
    # 节目单删除之后的一系列反应： 1、连接的区域时间处于未发布状态，（区域时间下节目单自动为None）
    ret = {"status": True}
    try:
        pk = request.GET.get("pk")
        programme = models.Programme.objects.filter(pk=pk).first()
        programme.areaintervaltime_set.all().update(is_publish=False)
        programme.delete()
    except Exception as e:
        ret["status"] = False
    return JsonResponse(ret)


def programme_publish(request):
    # 每个 manage 批准发布的只是其组下面的。
    ret = {"status": True, "msg": "发布成功！"}
    user = request.user
    try:
        pk = request.GET.get("pk")
        group = user.groups.all()[0]
        request_area = group.area_set.all()
        programme = models.Programme.objects.filter(pk=pk).first()
        for areaintervaltime in programme.areaintervaltime_set.all():
            if areaintervaltime.area in request_area:
                areaintervaltime.is_publish = True
                areaintervaltime.save()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "发布失败"
    return JsonResponse(ret)


def programme_unpublish(request):
    # 每个 manage 批准发布的只是其组下面的。
    ret = {"status": True, "msg": "取消发布成功！"}
    user = request.user
    try:
        pk = request.GET.get("pk")
        group = user.groups.all()[0]
        request_area = group.area_set.all()
        programme = models.Programme.objects.filter(pk=pk).first()
        for areaintervaltime in programme.areaintervaltime_set.all():
            if areaintervaltime.area in request_area:
                areaintervaltime.is_publish = False
                areaintervaltime.save()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "取消发布失败"
    return JsonResponse(ret)


def adv_programme_material_add(request, pk, user_pk):
    # 为节目单添加素材
    if request.method == "POST":
        materials = request.POST.getlist("materials")[0]
        materials = materials.split(",")
        programme_obj = models.AdvProgramme.objects.filter(pk=pk).first()
        ret = {"status": True, "msg": ""}
        try:
            for p, m in enumerate(materials):
                material_obj = models.MaterialFiles.objects.filter(pk=m).first()
                models.AdvProgrammeMaterial.objects.create(material=material_obj, programme=programme_obj, nid=p)
            ret["msg"] = "添加素材成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加素材失败！"
        return JsonResponse(ret)

    programme = models.AdvProgramme.objects.filter(pk=pk).first()
    adv_programme_materials = programme.advprogrammematerial_set.all().order_by("nid")

    user = models.UserInfo.objects.filter(pk=user_pk).first()
    files = models.MaterialFiles.objects.filter(user=user).order_by("-create_time")
    files, current_page = get_pg(request, files, 12)
    ret = {
        "files": files,
        "current_page": current_page,
        "pk": pk,
        "programme_materials": adv_programme_materials
    }

    return render(request, 'show_admin/programme_madd.html', ret)


@login_required
def adv_programme_editor(request, pk, user_pk):
    # 编辑广告节目单
    if request.method == "POST":
        sort_list = request.POST.getlist("sort_list")[0]
        sort_list = sort_list.split(",")
        ret = {"status": True}
        try:
            for s in sort_list:
                models.AdvProgrammeMaterial.objects.filter(id=int(s)).update(nid=sort_list.index(s))
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)
    ret = {
        "pk": pk,
        "user_pk": user_pk,
    }

    programme = models.AdvProgramme.objects.filter(pk=pk).first()
    if programme:
        ret["programme_materials"] = programme.advprogrammematerial_set.all().order_by("nid")
        ret["programme"] = programme
        # 选择时间
        intervals = models.IntervalTime.objects.all()
        # 选择区域，使用选项卡的形式
        user = models.UserInfo.objects.filter(pk=user_pk).first()
        groups = user.groups.all()
        areas = []
        for gp in groups:
            for area in gp.area_set.all():
                areas.append(area)
        ret["intervals"] = intervals
        ret["areas"] = areas
        ret["is_there"] = True
    else:
        ret["is_there"] = False
    return render(request, 'show_admin/programme_editor.html', ret)


def adv_programme_material_del(request):
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": "删除素材成功"}
    try:
        models.AdvProgrammeMaterial.objects.filter(pk=pk).delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除素材失败！"
    return JsonResponse(ret)


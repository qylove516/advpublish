from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models


def programme(request):
    if request.user.is_superuser:
        programmes = models.Programme.objects.all()
    else:
        programmes = models.Programme.objects.filter(user=request.user)

    ret = {
        "programmes": programmes,
    }
    return render(request, 'programme.html', ret)


def programme_add(request):
    if request.method == "POST":
        ret = {"status": True, "msg": ""}
        title = request.POST.get("title")
        try:
            if title:
                models.Programme.objects.create(title=title, user=request.user)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "新建节目单失败！"
        return JsonResponse(ret)
    # 取属于该用户的所有时间段
    user = request.user
    intervals = user.areaintervaltime_set.all()
    ret = {
        "intervals": intervals
    }
    return render(request, 'show_admin/programme_add.html', ret)


def programme_del(request):
    ret = {"status": True}
    try:
        pk = request.GET.get("pk")
        programme = models.Programme.objects.filter(pk=pk).first()
        programme.programmematerial_set.all().delete()
        programme.delete()
    except Exception as e:
        ret["status"] = False
    return JsonResponse(ret)


def programme_publish(request):
    ret = {"status": True}
    try:
        pk = request.GET.get("pk")
        programme = models.Programme.objects.filter(pk=pk).first()
        if not programme.is_publish:
            programme_interval_area = programme.areaintervaltime_set.all()
            programme_material = programme.programmematerial_set.all()
            if len(programme_material) == 0:
                ret["status"] = False
                ret["msg"] = "请先添加素材"
            elif len(programme_interval_area) == 0:
                ret["status"] = False
                ret["msg"] = "请先选择发布区域及时间"
            elif programme.is_review:
                models.Programme.objects.filter(pk=pk).update(is_publish=True)
            else:
                ret["status"] = False
                ret["msg"] = "请先提交审核！"
        else:
            models.Programme.objects.filter(pk=pk).update(is_publish=False)
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "发布失败"
    return JsonResponse(ret)


def programme_material_add(request, pk, username):
    # 为节目单添加素材
    if request.method == "POST":
        materials = request.POST.getlist("materials")[0]
        materials = materials.split(",")
        programme_obj = models.Programme.objects.filter(pk=pk).first()
        ret = {"status": True, "msg": ""}
        try:
            for p, m in enumerate(materials):
                material_obj = models.MaterialFiles.objects.filter(pk=m).first()
                models.ProgrammeMaterial.objects.create(material=material_obj, programme=programme_obj, nid=p)
            ret["msg"] = "添加素材成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加素材失败！"
        return JsonResponse(ret)

    programme = models.Programme.objects.filter(pk=pk).first()
    programme_materials = programme.programmematerial_set.all().order_by("nid")

    user = models.UserInfo.objects.filter(username=username).first()
    files = models.MaterialFiles.objects.filter(user=user).order_by("-create_time")

    ret = {
        "files": files,
        "pk": pk,
        "programme_materials": programme_materials
    }

    return render(request, 'show_admin/programme_material_add.html', ret)


@login_required
def programme_sort(request, pk, username):
    if request.method == "POST":
        sort_list = request.POST.getlist("sort_list")[0]
        sort_list = sort_list.split(",")
        ret = {"status": True}
        try:
            for s in sort_list:
                models.ProgrammeMaterial.objects.filter(id=int(s)).update(nid=sort_list.index(s))
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)
    ret = {}
    ret["pk"] = pk
    ret["username"] = username
    programme = models.Programme.objects.filter(pk=pk).first()
    if programme:
        programme_materials = programme.programmematerial_set.all().order_by("nid")
        ret["programme_materials"] = programme_materials
        programme_area_interval = programme.areaintervaltime_set.all()
        ret["programme"] = programme
        ret["programme_manage_materials"] = programme_area_interval
        ret["is_there"] = True
    else:
        ret["is_there"] = False
    return render(request, 'show_admin/programme_material_sort.html', ret)


def programme_material_del(request):
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": "删除素材成功"}
    try:
        models.ProgrammeMaterial.objects.filter(pk=pk).delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除素材失败！"
    return JsonResponse(ret)


def programme_manage_material(request, pk, username):
    # 提交审核，把每个所选择的区域时间字段中的programme赋值，并改变is_inuse的值
    if request.method == "POST":
        programme_area = request.POST.getlist("programme_area")[0]
        programme_area = programme_area.split(",")
        ret = {"status": True, "msg": "提交审核成功！"}
        try:
            programme = models.Programme.objects.filter(pk=pk).first()
            models.AreaIntervalTime.objects.filter(pk__in=programme_area).update(programme=programme, is_inuse=True)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "提交审核失败！"
        return JsonResponse(ret)
    user = models.UserInfo.objects.filter(username=username).first()
    area_interval = user.areaintervaltime_set.all()
    programme = models.Programme.objects.filter(pk=pk).first()
    # 判断有没有素材，如果有素材是可以提交审核，反之不可以
    if len(programme.programmematerial_set.all()) == 0:
        material_blank = True
    else:
        material_blank = False
    ret = {
        "material_blank": material_blank,
        "pk": pk,
        "username": username,
        "area_interval": area_interval
    }
    return render(request, 'show_admin/programme_manage_material.html', ret)


def programme_area_interval_del(request):
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": "删除区域时间成功"}
    try:
        models.AreaIntervalTime.objects.filter(pk=pk).update(programme=None, is_inuse=False)
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除区域时间失败！"
    return JsonResponse(ret)


def programme_manage_review(request):
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": ""}
    programme = models.Programme.objects.filter(pk=pk)
    try:
        if programme.first().is_review:
            programme.update(is_review=False)
        else:
            programme.update(is_review=True)
        ret["msg"] = "操成功！"
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "操失败！"
    return JsonResponse(ret)

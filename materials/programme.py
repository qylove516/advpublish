from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    # 取每个节目单的 programme material

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


def programme_material_add(request, nid, username):
    # 添加
    if request.method == "POST":
        materials = request.POST.getlist("materials")[0]
        materials = materials.split(",")
        programme_obj = models.Programme.objects.filter(nid=nid).first()
        ret = {"status": True, "msg": ""}
        try:
            for m in materials:
                material_obj = models.MaterialFiles.objects.filter(pk=m).first()
                models.ProgrammeMaterial.objects.create(material=material_obj, programme=programme_obj)
            ret["msg"] = "添加素材成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加素材失败！"
        return JsonResponse(ret)

    user = models.UserInfo.objects.filter(username=username).first()
    files = models.MaterialFiles.objects.filter(user=user).order_by("-create_time")
    ret = {
        "files": files,
        "nid": nid
    }

    return render(request, 'show_admin/programme_material_add.html', ret)


def programme_sort(request, nid):
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
    programme = models.Programme.objects.filter(nid=nid).first()
    programme_materials = programme.programmematerial_set.all().order_by("nid")
    ret = {
        "nid": nid,
        "programme_materials": programme_materials
    }
    return render(request, 'show_admin/programme_material_sort.html', ret)


def programme_material_del(request, pk):
    if request.method == "POST":
        programme_materials = request.POST.getlist("programme_materials")[0]
        programme_materials = programme_materials.split(",")
        ret = {"status": True, "msg": ""}
        try:
            for m in programme_materials:
                models.ProgrammeMaterial.objects.filter(pk=m).delete()
            ret["msg"] = "添加素材成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加素材失败！"
        return JsonResponse(ret)
    programme = models.Programme.objects.filter(nid=pk).first()
    programme_materials = programme.programmematerial_set.all().order_by("nid")
    ret = {
        "pk": pk,
        "programme_materials": programme_materials
    }
    return render(request, 'show_admin/programme_material_del.html', ret)

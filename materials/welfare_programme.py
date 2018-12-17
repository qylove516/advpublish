from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from materials.get_pgs import get_pg
from django.db.models import Q


def welfare_programme_primary(request):
    # 公益主屏
    user = request.user
    welfare_programmes = None
    if user.is_manage:
        welfare_programmes = models.PrimaryWelfareProgramme.objects.filter(user=user)
    elif user.is_superuser:
        welfare_programmes = models.PrimaryWelfareProgramme.objects.all()
    ret = {
        "welfare_programmes": welfare_programmes,
        "user_pk": user.pk,
    }
    return render(request, 'welfare/welfare_programme_primary.html', ret)


def welfare_programme_primary_add(request):
    user = request.user
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": "创建成功！"}
        welfare_programme = models.PrimaryWelfareProgramme.objects.filter(title=title).first()
        if welfare_programme:
            ret["status"] = False
            ret["msg"] = "此标题已存在！"
        else:
            try:
                models.PrimaryWelfareProgramme.objects.create(title=title, user=user)
            except Exception as e:
                ret["status"] = False
                ret["msg"] = "创建失败！"
        return JsonResponse(ret)
    return render(request, "welfare/welfare_programme_primary_add.html")


def welfare_programme_primary_del(request):
    welfare_programme_pk = request.GET.get("welfare_programme_pk")
    ret = {
        "status": True,
        "msg": "删除成功！"
    }
    try:
        models.PrimaryWelfareProgramme.objects.filter(pk=welfare_programme_pk).delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


# 公益主屏编辑
@login_required
def welfare_programme_primary_editor(request, programme_pk, user_pk):
    if request.method == "POST":
        sort_list = request.POST.getlist("sort_list")[0]
        sort_list = sort_list.split(",")
        ret = {"status": True}
        try:
            for s in sort_list:
                models.PrimaryWelfareProgrammeMaterial.objects.filter(id=int(s)).update(nid=sort_list.index(s))
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)
    welfare_primary_materials = models.PrimaryWelfareProgrammeMaterial.objects.filter(
        programme_id=programme_pk).order_by("nid")
    welfare_primary_programme = models.PrimaryWelfareProgramme.objects.filter(pk=programme_pk).first()
    files = models.MaterialFiles.objects.filter(user_id=user_pk).order_by("-create_time")
    files, current_page = get_pg(request, files, 8)
    ret = {
        "welfare_primary_programme": welfare_primary_programme,  # 节目单
        "welfare_primary_materials": welfare_primary_materials,  # 节目单临时素材
        "is_play_time": True,
        "programme_pk": programme_pk,
        "current_page": current_page,
        "user_pk": user_pk,
        "files": files,
    }
    return render(request, 'welfare/welfare_programme_primary_editor.html', ret)


# 公益主屏添加临时素材
def welfare_primary_material_add(request, welfare_programme_pk):
    if request.method == "POST":
        materials = request.POST.getlist("materials")[0]
        materials = materials.split(",")
        m_length = len(materials)
        welfare_programme = models.PrimaryWelfareProgramme.objects.filter(pk=welfare_programme_pk).first()
        p_materials = models.PrimaryWelfareProgrammeMaterial.objects.filter(programme_id=welfare_programme_pk)
        for k in p_materials:
            nid = k.nid
            k.nid = nid + m_length
            k.save()
        ret = {
            "status": True,
            "msg": "添加素材成功！"
        }
        if welfare_programme:
            try:
                for p, m in enumerate(materials):
                    material_obj = models.MaterialFiles.objects.filter(pk=m).first()
                    models.PrimaryWelfareProgrammeMaterial.objects.create(
                        programme=welfare_programme,
                        material=material_obj,
                        nid=p
                    )
            except Exception as e:
                ret["status"] = False
                ret["msg"] = "添加素材失败"
        return JsonResponse(ret)


# 删除节目单临时素材
def welfare_ppm_del(request):
    material_pk = request.GET.get("material_pk")
    programme_pk = request.GET.get("programme_pk")
    material_nid = models.PrimaryWelfareProgrammeMaterial.objects.filter(pk=material_pk).first().nid
    p_materials = models.PrimaryWelfareProgrammeMaterial.objects.filter(Q(programme_id=programme_pk),
                                                                        Q(nid__gt=material_nid))
    ret = {
        "status": True,
        "msg": "删除成功！"
    }
    for k in p_materials:
        nid = k.nid
        k.nid = nid - 1
        k.save()
    try:
        models.PrimaryWelfareProgrammeMaterial.objects.filter(pk=material_pk).delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def welfare_primary_material_change_time(request):
    material_pk = request.GET.get("material_pk")
    play_time = request.GET.get("play_time")
    ret = {
        "status": True,
        "msg": "修改成功"
    }
    try:
        models.PrimaryWelfareProgrammeMaterial.objects.filter(pk=material_pk).update(play_time=play_time)
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "修改失败！"
    return JsonResponse(ret)


# 查看公益节目
def welfare_programme_view(request, programme_pk):
    programme = models.PrimaryWelfareProgramme.objects.filter(pk=programme_pk).first()
    programme_materials = models.PrimaryWelfareProgrammeMaterial.objects.filter(programme_id=programme_pk)
    ret = {
        "is_play_time": True,
        "programme": programme,
        "programme_materials": programme_materials
    }
    return render(request, "include/programme_view.html", ret)


# 公益节目单与设备
def welfare_programme_machine(request, machine_nid):
    ret = {
        "machine_nid": machine_nid,
    }
    if request.user.is_manage:
        welfare_programmes = models.PrimaryWelfareProgramme.objects.filter(user_id=request.user.pk)
        ret["welfare_programmes"] = welfare_programmes

    return render(request, "welfare/welfare_programme_machine.html", ret)


def welfare_programme_secondary(request):
    pass

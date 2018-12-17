from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from materials.get_pgs import get_pg
from django.db.models import Q


# 普通用户在区域列表中查看是否已通过审请
def adv_programme(request):
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


# 广告商添加广告节目
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


# 广告节目单删除
def adv_programme_del(request):
    ret = {"status": True}
    try:
        adv_programme_pk = request.GET.get("adv_programme_pk")
        models.AdvProgramme.objects.filter(pk=adv_programme_pk).delete()
    except Exception as e:
        ret["status"] = False
    return JsonResponse(ret)


# 编辑广告节目单,此处的 user_pk 即是相应的节目单所属用户的 id
@login_required
def adv_programme_editor(request, adv_programme_pk, user_pk):
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
        "adv_programme_pk": adv_programme_pk,
        "user_pk": user_pk,
    }
    adv_programmes = models.AdvProgramme.objects.filter(pk=adv_programme_pk).first()
    user = models.UserInfo.objects.filter(pk=user_pk).first()
    files = models.MaterialFiles.objects.filter(user=user).order_by("-create_time")
    files, current_page = get_pg(request, files, 8)
    if adv_programme:
        ret["adv_programme_materials"] = adv_programmes.advprogrammematerial_set.all().order_by("nid")
        ret["adv_programmes"] = adv_programmes
        ret["files"] = files
        ret["current_page"] = current_page
        ret["is_play_time"] = True

    return render(request, 'show_admin/programme_editor.html', ret)


# 为节目单添加素材
def adv_programme_material_add(request, programme_pk):
    if request.method == "POST":
        materials = request.POST.getlist("materials")[0]
        materials = materials.split(",")
        m_length = len(materials)
        programme_obj = models.AdvProgramme.objects.filter(pk=programme_pk).first()
        p_materials = models.AdvProgrammeMaterial.objects.filter(programme_id=programme_pk)
        for k in p_materials:
            nid = k.nid
            k.nid = nid + m_length
            k.save()
        ret = {
            "status": True,
            "msg": "添加素材成功！"
        }
        try:
            for p, m in enumerate(materials):
                material_obj = models.MaterialFiles.objects.filter(pk=m).first()
                models.AdvProgrammeMaterial.objects.create(material=material_obj, programme=programme_obj, nid=p)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加素材失败！"
        return JsonResponse(ret)


# 删除节目单临时素材
def adv_programme_material_del(request):
    material_pk = request.GET.get("material_pk")
    programme_pk = request.GET.get("programme_pk")
    material_nid = models.AdvProgrammeMaterial.objects.filter(pk=material_pk).first().nid
    p_materials = models.AdvProgrammeMaterial.objects.filter(Q(programme_id=programme_pk),
                                                                        Q(nid__gt=material_nid))
    ret = {
        "status": True,
        "msg": "删除素材成功"
    }
    for k in p_materials:
        nid = k.nid
        k.nid = nid - 1
        k.save()
    try:
        models.AdvProgrammeMaterial.objects.filter(pk=material_pk).delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除素材失败！"
    return JsonResponse(ret)


# 修改临时素材图片播放的时间
def programme_change_time(request):
    material_related_pk = request.GET.get("material_related_pk")
    play_time = request.GET.get("play_time")
    ret = {"status": True, "msg": "修改成功！"}
    try:
        models.AdvProgrammeMaterial.objects.filter(pk=material_related_pk).update(play_time=play_time)
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "修改失败！"
    return JsonResponse(ret)


# 查看节目单内容
def programme_view(request, programme_pk):
    programme = models.AdvProgramme.objects.filter(pk=programme_pk).first()
    programme_materials = models.AdvProgrammeMaterial.objects.filter(programme_id=programme_pk)
    ret = {
        "is_play_time": True,
        "programme": programme,
        "programme_materials": programme_materials
    }
    return render(request, "include/programme_view.html", ret)

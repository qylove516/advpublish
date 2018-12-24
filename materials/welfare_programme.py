from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from materials.utils.programme import Programme, ProgrammeMaterial


def welfare_primary_programme(request):
    # 公益主屏
    ret = Programme(request, models.PrimaryWelfareProgramme.objects).detail("welfare_primary")
    return render(request, 'welfare/welfare_primary_programme.html', ret)


def welfare_primary_programme_add(request):
    if request.method == "POST":
        ret = Programme(request, models.PrimaryWelfareProgramme.objects).add()
        return JsonResponse(ret)
    else:
        return render(request, "welfare/welfare_primary_programme_add.html")


def welfare_primary_programme_del(request):
    ret = Programme(request, models.PrimaryWelfareProgramme.objects).delete()
    return JsonResponse(ret)


# 公益主屏编辑
@login_required
def welfare_primary_programme_editor(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).editor(programme_pk, "welfare_primary", is_play_time=True)
        return JsonResponse(ret)
    else:
        ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).editor(programme_pk, "welfare_primary", is_play_time=True)
        return render(request, 'welfare/welfare_primary_programme_editor.html', ret)


# 公益主屏添加临时素材
def welfare_primary_material_add(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).add(programme_pk, "welfare_primary")
        return JsonResponse(ret)


# 删除公益主屏临时素材
def welfare_primary_material_del(request):
    ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).delete()
    return JsonResponse(ret)


def welfare_primary_material_change_time(request):
    ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).change_time()
    return JsonResponse(ret)


# 查看公益节目
def welfare_primary_material_view(request, programme_pk):
    ret = ProgrammeMaterial(request, models.PrimaryWelfareProgrammeMaterial.objects).programme_view(programme_pk, "welfare_primary", is_play_time=True)
    return render(request, "include/programme_view.html", ret)


# 公益副屏
def welfare_secondary_programme(request):
    ret = Programme(request, models.SecondaryWelfareProgramme.objects).detail("welfare_primary")
    return render(request, 'welfare/welfare_secondary_programme.html', ret)


# 公益副屏添加节目单
def welfare_secondary_programme_add(request):
    if request.method == "POST":
        ret = Programme(request, models.SecondaryWelfareProgramme.objects).add()
        return JsonResponse(ret)
    return render(request, "welfare/welfare_secondary_programme_add.html")


# 删除副屏节目单
def welfare_secondary_programme_del(request):
    ret = Programme(request, models.SecondaryWelfareProgramme.objects).delete()
    return JsonResponse(ret)


# 节目单编辑
@login_required
def welfare_secondary_material_editor(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.SecondaryWelfareProgrammeMaterial.objects).editor(programme_pk, "welfare_secondary", is_play_time=False)
        return JsonResponse(ret)
    else:
        ret = ProgrammeMaterial(request, models.SecondaryWelfareProgrammeMaterial.objects).editor(programme_pk, "welfare_secondary", is_play_time=False)
        return render(request, 'welfare/welfare_secondary_programme_editor.html', ret)


# 公益副屏节目单素材添加
def welfare_secondary_material_add(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.SecondaryWelfareProgrammeMaterial.objects).add(programme_pk, "welfare_secondary")
        return JsonResponse(ret)


# 删除公益副屏节目素材
def welfare_secondary_material_del(request):
    ret = ProgrammeMaterial(request, models.SecondaryWelfareProgrammeMaterial.objects).delete()
    return JsonResponse(ret)


def welfare_secondary_material_view(request, programme_pk):
    ret = ProgrammeMaterial(request, models.SecondaryWelfareProgrammeMaterial.objects).programme_view(programme_pk, "welfare_secondary", is_play_time=False)
    return render(request, "include/programme_view.html", ret)


# 公益节目单与设备
def welfare_programme_machine(request, machine_nid):
    if request.method == "POST":
        primary_programme = request.POST.get("primary_programme")
        secondary_programme = request.POST.get("secondary_programme")
        qrcode_programme = request.POST.get("qrcode_programme")
        machine_template = request.POST.get("machine_template")
        ret = {"status": True, "msg": "创建成功！"}
        try:
            primary = models.PrimaryWelfareProgrammeRelated.objects.filter(machine_id=machine_nid)
            if primary.first():
                primary.update(programme_id=primary_programme)
            else:
                models.PrimaryWelfareProgrammeRelated.objects.create(programme_id=primary_programme, machine_id=machine_nid)
            secondary = models.SecondaryWelfareProgrammeRelated.objects.filter(machine_id=machine_nid)
            if secondary.first():
                secondary.update(welfare_programme_id=secondary_programme)
            else:
                models.SecondaryWelfareProgrammeRelated.objects.create(welfare_programme_id=secondary_programme, machine_id=machine_nid)
            qrcode = models.QrCodeProgrammeRelated.objects.filter(machine_id=machine_nid)
            if qrcode.first():
                qrcode.update(programme_id=qrcode_programme)
            else:
                models.QrCodeProgrammeRelated.objects.create(programme_id=qrcode_programme, machine_id=machine_nid)
            template = models.MachineTemplateRelated.objects.filter(machine_id=machine_nid)
            if template.first():
                qrcode.update(programme_id=machine_template)
            else:
                models.MachineTemplateRelated.objects.create(programme_id=machine_template, machine_id=machine_nid)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "创建失败！"
        return JsonResponse(ret)
    ret = {
        "machine_nid": machine_nid,
        "machine_title": models.Machine.objects.filter(nid=machine_nid).first().title,
    }

    if request.user.is_manage:
        welfare_primary_programmes = models.PrimaryWelfareProgramme.objects.filter(user_id=request.user.pk)
        welfare_secondary_programmes = models.SecondaryWelfareProgramme.objects.filter(user_id=request.user.pk)
        qrcode_programmes = models.QrCodeProgramme.objects.filter(user_id=request.user.pk)
        machine_template = models.MachineTemplate.objects.filter(user_id=request.user.pk)
        is_primary = models.PrimaryWelfareProgrammeRelated.objects.filter(machine__nid=machine_nid).first()
        is_secondary = models.SecondaryWelfareProgrammeRelated.objects.filter(machine__nid=machine_nid).first()
        is_qrcode = models.QrCodeProgrammeRelated.objects.filter(machine__nid=machine_nid).first()
        is_template = models.MachineTemplateRelated.objects.filter(machine__nid=machine_nid).first()
        ret["welfare_primary_programmes"] = welfare_primary_programmes
        ret['welfare_secondary_programmes'] = welfare_secondary_programmes
        ret["qrcode_programmes"] = qrcode_programmes
        ret["machine_template"] = machine_template
        ret["is_primary"] = is_primary
        ret["is_secondary"] = is_secondary
        ret["is_qrcode"] = is_qrcode
        ret["is_template"] = is_template
    return render(request, "welfare/welfare_programme_machine.html", ret)

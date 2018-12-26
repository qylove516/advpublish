from materials import models
from materials.utils.programme import Programme, ProgrammeMaterial
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# 二维码节目单
def qrcode_programme(request):
    ret = Programme(request, models.QrCodeProgramme.objects).detail("qrcode")
    return render(request, "qrcode/qrcode_programme.html", ret)


# 添加节目单
def qrcode_programme_add(request):
    if request.method == "POST":
        ret = Programme(request, models.QrCodeProgramme.objects).add()
        return JsonResponse(ret)
    else:
        return render(request, "qrcode/qrcode_programme_add.html")


# 删除节目单
def qrcode_programme_del(request):
    ret = Programme(request, models.QrCodeProgramme.objects).delete()
    return JsonResponse(ret)


# 节目单编辑
@login_required
def qrcode_programme_editor(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.QrCodeProgrammeMaterial.objects).editor(programme_pk, "qrcode", is_play_time=False)
        return JsonResponse(ret)
    else:
        ret = ProgrammeMaterial(request, models.QrCodeProgrammeMaterial.objects).editor(programme_pk, "qrcode", is_play_time=False)
        return render(request, "qrcode/qrcode_programme_editor.html", ret)


# 素材添加
def qrcode_material_add(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.QrCodeProgrammeMaterial.objects).add(programme_pk, "qrcode")
        return JsonResponse(ret)


# 素材删除
def qrcode_material_del(request):
    ret = ProgrammeMaterial(request, models.QrCodeProgrammeMaterial.objects).delete()
    return JsonResponse(ret)


# 查看
def qrcode_material_view(request, programme_pk):
    ret = ProgrammeMaterial(request, models.QrCodeProgrammeMaterial.objects).programme_view(programme_pk, "qrcode", is_play_time=False)
    return render(request, "include/programme_view.html", ret)


# 设备模板
def machine_template(request):
    ret = Programme(request, models.MachineTemplate.objects).detail("template")
    return render(request, "qrcode/machine_template.html", ret)


# 添加模板
def machine_template_add(request):
    if request.method == "POST":
        ret = Programme(request, models.MachineTemplate.objects).add()
        return JsonResponse(ret)
    else:
        return render(request, "qrcode/machine_template_add.html")


# 删除模板
def machine_template_del(request):
    ret = Programme(request, models.MachineTemplate.objects).delete()
    return JsonResponse(ret)


# 编辑模板
@login_required
def machine_template_editor(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.MachineTemplateMaterial.objects).editor(programme_pk, "template", is_play_time=False)
        return JsonResponse(ret)
    else:
        ret = ProgrammeMaterial(request, models.MachineTemplateMaterial.objects).editor(programme_pk, "template", is_play_time=False)
        return render(request, "qrcode/machine_template_editor.html", ret)


# 添加模板素材
def machine_material_add(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.MachineTemplateMaterial.objects).add(programme_pk, "template")
        return JsonResponse(ret)


# 模板素材删除
def machine_material_del(request):
    ret = ProgrammeMaterial(request, models.MachineTemplateMaterial.objects).delete()
    return JsonResponse(ret)


# 查看模板
def machine_material_view(request, programme_pk):
    ret = ProgrammeMaterial(request, models.MachineTemplateMaterial.objects).programme_view(programme_pk, "template", is_play_time=False)
    return render(request, "include/programme_view.html", ret)

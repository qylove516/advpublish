from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from materials.utils.programme import Programme, ProgrammeMaterial


# 普通用户在区域列表中查看是否已通过审请
def adv_programme(request):
    ret = Programme(request, models.AdvProgramme.objects).detail("adv")
    return render(request, 'adv/adv_programme.html', ret)


# 广告商添加广告节目
def adv_programme_add(request):
    if request.method == "POST":
        ret = Programme(request, models.AdvProgramme.objects).add()
        return JsonResponse(ret)
    else:
        return render(request, 'adv/adv_programme_add.html')


# 广告节目单删除
def adv_programme_del(request):
    ret = Programme(request, models.AdvProgramme.objects).delete()
    return JsonResponse(ret)


# 编辑广告节目单,此处的 user_pk 即是相应的节目单所属用户的 id
@login_required
def adv_programme_editor(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).editor(programme_pk, "adv")
        return JsonResponse(ret)
    else:
        ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).editor(programme_pk, "adv")
        return render(request, 'adv/adv_programme_editor.html', ret)


# 为节目单添加素材
def adv_programme_material_add(request, programme_pk):
    if request.method == "POST":
        ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).add(programme_pk, "adv")
        return JsonResponse(ret)


# 删除节目单临时素材
def adv_programme_material_del(request):
    ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).delete()
    return JsonResponse(ret)


# 修改临时素材图片播放的时间
def programme_change_time(request):
    ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).change_time()
    return JsonResponse(ret)


# 查看节目单内容
def programme_view(request, programme_pk):
    ret = ProgrammeMaterial(request, models.AdvProgrammeMaterial.objects).programme_view(programme_pk, "adv")
    return render(request, "include/programme_view.html", ret)

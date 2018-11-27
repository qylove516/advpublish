from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from advpublish.settings import SUPPLIERS


def areas(request):
    areas = models.Area.objects.annotate()
    ret = {
        'areas': areas,
    }
    return render(request, 'areas.html', ret)


def areas_add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": ""}
        try:
            area = models.Area.objects.create(title=title)
            intervals = models.IntervalTime.objects.all()
            for i in intervals:
                models.AreaIntervalTime.objects.create(area=area, interval_time=i)
        except Exception as e:
            ret["msg"] = "添加标签失败！"
        return JsonResponse(ret)
    ret = {
        "areas": areas,
    }
    return render(request, 'show_admin/areas_add.html', ret)


def areas_update(request, pk):
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": ""}
        try:
            models.Area.objects.filter(pk=pk).update(title=title)
            ret["msg"] = "修改成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "修改失败！"
        return JsonResponse(ret)
    area = models.Area.objects.filter(pk=pk).first()
    ret = {
        'pk': pk,
        'area': area
    }
    return render(request, 'show_admin/areas_update.html', ret)


def areas_del(request):
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": ""}
    try:
        area = models.Area.objects.filter(pk=pk)
        area.first().machine_set.all().delete()
        area.first().areaintervaltime_set.all().delete()
        area.delete()
        ret["msg"] = "删除成功！"
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def machine_area(request, area_pk):
    if request.method == 'POST':
        nid = request.POST.get("nid")
        ret = {
            "status": True
        }
        try:
            models.Machine.objects.filter(nid=nid).delete()
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)

    area = models.Area.objects.filter(pk=area_pk).first()
    machines = area.machine_set.all()
    ret = {
        'area_pk': area_pk,
        'machines': machines
    }
    return render(request, 'machines.html', ret)


def machines_add(request, area_pk):
    if request.method == "POST":
        title = request.POST.get("title")
        nid = request.POST.get("nid")
        ret = {"status": True, "msg": ""}
        position = request.POST.get("position")
        # area = request.POST.get("area")
        supplier = request.POST.get("supplier")
        # area = models.Area.objects.filter(title=area).first()
        try:
            machine = models.Machine.objects.filter(nid=nid).first()
            if machine:
                ret["status"] = False
                ret["msg"] = "该设备已存在！"
                return JsonResponse(ret)
            area = models.Area.objects.filter(pk=area_pk).first()
            models.Machine.objects.create(nid=nid, title=title, position=position, area=area, supplier=supplier)
            ret["msg"] = "创建设备成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "创建设备失败！"
        return JsonResponse(ret)
    # areas = models.Area.objects.all()
    ret = {
        'area_pk': area_pk,
        'suppliers': SUPPLIERS
    }
    return render(request, 'show_admin/machines_add.html', ret)


def machine_detail(request, nid):
    machine = models.Machine.objects.filter(nid=nid).first()
    ret = {
        "machine": machine
    }
    return render(request, 'show_admin/machine_detail.html', ret)


def machine_update(request, nid):
    if request.method == "POST":
        title = request.POST.get("title")
        position = request.POST.get("position")
        ret = {"status": True, "msg": ""}
        try:
            models.Machine.objects.filter(nid=nid).update(title=title, position=position)
            ret["msg"] = "创建设备成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "创建设备失败！"
        return JsonResponse(ret)
    machine = models.Machine.objects.filter(nid=nid).first()
    ret = {
        "machine": machine
    }
    return render(request, 'show_admin/machine_update.html', ret)

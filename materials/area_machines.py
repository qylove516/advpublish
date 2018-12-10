from django.http import JsonResponse
from django.shortcuts import render
from materials import models
from advpublish.settings import SUPPLIERS
from materials.get_pgs import get_pg


def areas_get(request):
    # 展示终端区域
    areas_all = models.Area.objects.all().order_by("title")
    areas, current_page = get_pg(request, areas_all, 8)
    ret = {
        "areas_all": areas_all,
        'areas': areas,
        "current_page": current_page
    }
    return render(request, 'areas.html', ret)


def areas_add(request):
    # 添加终端设备区域
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": "添加区域成功"}
        try:
            models.Area.objects.create(title=title)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加区域失败！"
        return JsonResponse(ret)
    return render(request, 'show_admin/areas_add.html')


def areas_update(request, pk):
    # 修改终端区域的名称
    if request.method == "POST":
        title = request.POST.get("title")
        ret = {"status": True, "msg": "修改成功！"}
        try:
            models.Area.objects.filter(pk=pk).update(title=title)
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
    # 终端区域：删除区域
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": "删除成功！"}
    try:
        models.Area.objects.filter(pk=pk).delete()
        # 区域删除之后，区域下的设备也会自动删除，设备对应的设备时间模型也会删除
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def machine_list(request, area_pk):
    # 区域列表：删除设备
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
    if area:
        machines_all = area.machine_set.all().order_by("area_id")
        machines, current_page = get_pg(request, machines_all, 8)
        ret = {
            'area_pk': area_pk,
            "machines_all": machines_all,
            'machines': machines,
            "current_page": current_page
        }
        return render(request, 'machines.html', ret)
    else:
        return render(request, 'error/404.html')


def machines_add(request, area_pk):
    # 区域列表：增加设备
    if request.method == "POST":
        title = request.POST.get("title")
        nid = request.POST.get("nid")
        ret = {"status": True, "msg": ""}
        position = request.POST.get("position")
        supplier = request.POST.get("supplier")
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
    ret = {
        'area_pk': area_pk,
        'suppliers': SUPPLIERS
    }
    return render(request, 'show_admin/machines_add.html', ret)


def machine_addpi(request, nid):
    if request.method == "POST":
        intervals = request.POST.getlist("intervals")[0]
        intervals = intervals.split(",")
        programme_pk = request.POST.get("programme_pk")
        ret = {"status": True, "msg": "添加成功！"}
        try:
            programme = models.AdvProgramme.objects.filter(pk=programme_pk).first()
            machine = models.Machine.objects.filter(nid=nid).first()
            title = programme.title + nid
            rd = models.AdvProgrammeRelated.objects.filter(title=title).first()
            if not rd:
                models.AdvProgrammeRelated.objects.create(title=title, machine=machine, programme=programme)
                rd = models.AdvProgrammeRelated.objects.filter(title=title).first()
            # rd.update(machine=machine)
            rd.interval.add(*intervals)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加失败！"
        return JsonResponse(ret)
    machine = models.Machine.objects.filter(nid=nid).first()
    machine_related = machine.advprogrammerelated_set.all()
    interval_times = []
    for m in machine_related:
        for k in m.interval.all():
            interval_times.append(k)
    intervals = models.IntervalTime.objects.all()
    interval_times = list(set(intervals) ^ set(interval_times))
    programmes = models.AdvProgramme.objects.filter(user=request.user)
    ret = {
        "machine_nid": nid,
        "interval_times": interval_times,
        "programmes": programmes
    }
    return render(request, "show_admin/machine_addpi.html", ret)


def machine_detail(request, nid):
    machine = models.Machine.objects.filter(nid=nid).first()
    ret = {
        "machine": machine
    }
    return render(request, 'show_admin/machine_detail.html', ret)


def machine_update(request, nid):
    # 更新设备信息,
    if request.method == "POST":
        title = request.POST.get("title")
        area = request.POST.get("area")
        position = request.POST.get("position")
        ret = {"status": True, "msg": ""}
        try:
            area = models.Area.objects.filter(title=area).first()
            if not area:
                ret["status"] = False
                ret["msg"] = "请确认区域名称是否存在！"
                return JsonResponse(ret)
            models.Machine.objects.filter(nid=nid).update(title=title, position=position, area=area)
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

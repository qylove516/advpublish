from materials import models
from django.shortcuts import render, HttpResponse
import json
from django.http import JsonResponse


def manage_area(request, username, area_pk):
    if request.method == "POST":
        area_interval_obj = request.POST.get("area_interval")
        area_interval = area_interval_obj.split(",")
        user = models.UserInfo.objects.filter(username=username).first()
        ret = {"status": True, "msg": ""}
        try:
            for k in area_interval:
                models.AreaIntervalTime.objects.filter(pk=int(k)).update(user=user, is_selected=True)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "出错啦！"
        return JsonResponse(ret)
    area_interval = models.Area.objects.filter(pk=area_pk).first()
    area_interval = area_interval.areaintervaltime_set.all()
    ret = {
        'username': username,
        'area_interval': area_interval
    }
    return render(request, 'show_admin/manage_area.html', ret)


def manage_machine(request, username):
    if request.method == "POST":
        pk = request.POST.get("pk")
        ret = {"status": True}
        if pk:
            try:
                models.AreaIntervalTime.objects.filter(pk=pk).update(user=None, is_selected=False)
            except Exception as e:
                ret["status"] = False
        else:
            ret["status"] = False
        return JsonResponse(ret)
    # 为用户分配时间区域
    areas = models.Area.objects.all()
    user = models.UserInfo.objects.filter(username=username).first()
    area_intervals = user.areaintervaltime_set.all()
    ret = {
        "username": username,
        "areas": areas,
        "area_intervals": area_intervals,
    }
    return render(request, 'manage_machine.html', ret)

from materials import models
from django.shortcuts import render, HttpResponse
import json
from django.http import JsonResponse


def manage_machine(request, username):
    # 为用户分配设备时间，先选择区域，再选择时间
    areas = models.Area.objects.all()
    ret = {
        "username": username,
        "areas": areas
    }
    return render(request, 'manage_machine.html', ret)


def manage_area(request, username, area_pk):
    if request.method == "POST":
        area_interval_obj = request.POST.get("area_interval")
        area_interval = area_interval_obj.split(",")
        user = models.UserInfo.objects.filter(username=username).first()
        ret = {"status": True, "msg": ""}
        try:
            for k in area_interval:
                models.AreaIntervalTime.objects.filter(pk=int(k)).update(user=user, is_blank=True)
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

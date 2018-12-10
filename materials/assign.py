from materials import models
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse


def db_area(request, group_pk):
    #
    if request.method == "POST":
        area_pk = request.POST.get("area_pk")
        ret = {"status": True}
        try:
            area_obj = models.Area.objects.filter(pk=area_pk)
            area_obj.update(group=None, is_selected=False)
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)
    group = models.Group.objects.filter(pk=group_pk).first()
    areas = group.area_set.all().order_by("title")
    ret = {
        "group_pk": group_pk,
        "areas": areas
    }
    return render(request, 'db_area.html', ret)


def assign_area(request, pk):
    if request.method == "POST":
        areas = request.POST.getlist("assign_areas")[0]
        areas = areas.split(",")
        group = models.Group.objects.filter(pk=pk).first()
        ret = {"status": True, "msg": "添加成功！"}
        # 如果areas中存在数据
        if areas[0]:
            try:
                for p in areas:
                    models.Area.objects.filter(pk=p).update(group=group, is_selected=True)
            except Exception as e:
                ret["status"] = False
                ret["msg"] = "添加失败！"
        else:
            ret["status"] = False
            ret["msg"] = "没有选中区域，添加失败！"
        return JsonResponse(ret)
    areas = models.Area.objects.all()
    ret = {
        "pk": pk,
        "areas": areas
    }
    return render(request, 'show_admin/assign_area.html', ret)


"""
def assign_time(request, user_pk, area_pk):
    # 时间分配：为用户分配区域时间
    if request.method == "POST":
        area_interval_obj = request.POST.get("area_interval")
        area_interval = area_interval_obj.split(",")
        user = models.UserInfo.objects.filter(pk=user_pk).first()
        ret = {"status": True, "msg": ""}
        try:
            models.AreaIntervalTime.objects.filter(pk__in=area_interval).update(user=user, is_selected=True)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "出错啦！"
        return JsonResponse(ret)
    area_interval = models.Area.objects.filter(pk=area_pk).first()
    area_interval = area_interval.areaintervaltime_set.all()
    ret = {
        'user_pk': user_pk,
        'area_interval': area_interval
    }
    return render(request, 'show_admin/assign_time.html', ret)



def db_time(request, user_pk):
    # 时间分配：删除用户有此地的权限
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
    # 获取该用户拥有的时间
    areas = []
    if request.user.is_manage:
        groups_request = request.user.groups.all()
        groups_selected = models.UserInfo.objects.filter(pk=user_pk).first().groups.all()
        groups = list(set(groups_request).intersection(set(groups_selected)))
        for g in groups:
            areas.extend(g.area_set.all())
    else:
        groups = models.UserInfo.objects.filter(pk=user_pk).first().groups.all()
        for g in groups:
            areas.extend(g.area_set.all().filter())
    user = models.UserInfo.objects.filter(pk=user_pk).first()
    # TODO 过滤
    area_intervals = []
    for a in areas:
        area_intervals.extend(a.areaintervaltime_set.all().filter(user=user))
    ret = {
        "user_pk": user_pk,
        "areas": areas,
        "area_intervals": area_intervals,
    }
    return render(request, 'db_time.html', ret)
"""

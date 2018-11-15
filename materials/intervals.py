from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from materials import models
from django.db.models import Q


def intervals(request):
    intervals_all = models.IntervalTime.objects.all()
    ret = {
        "intervals": intervals_all
    }
    return render(request, 'intervals.html', ret)


def intervals_add(request):
    if request.method == "POST":
        username = request.POST.get("user")
        user = models.UserInfo.objects.filter(username=username).first()
        intervals = request.POST.getlist("intervals")[0]
        intervals = intervals.split(",")
        ret = {"status": True, "msg": ""}
        try:
            for i in intervals:
                k = models.IntervalTime.objects.filter(interval=i).first()
                k.user = user
                k.save()
            ret["msg"] = "添加用户成功！"
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加用户失败！"
        return JsonResponse(ret)
    users = models.UserInfo.objects.filter(is_staff=True)
    intervals_all = models.IntervalTime.objects.all()
    intervals_used = models.IntervalTime.objects.filter(Q(user__is_staff=True))
    intervals_get = list(set(intervals_all) ^ set(intervals_used))
    ret = {
        "users": users,
        "intervals": intervals_get
    }
    return render(request, 'show_admin/intervals_add.html', ret)


def intervals_del(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        ret = {"status": True}
        try:
            interval = models.IntervalTime.objects.filter(nid=nid).first()
            interval.user = None
            interval.save()
        except Exception as e:
            ret["status"] = False
        return JsonResponse(ret)

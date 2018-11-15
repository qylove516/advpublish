from django.http import JsonResponse
from django.shortcuts import render
from materials import models


def programme_add(request):
    if request.method == "POST":
        ret = {"status": False, "msg": ""}
        title = request.POST.get("title")
        intervals = request.POST.getlist("intervals")[0]
        intervals = intervals.split(",")
        try:
            programme_obj = None
            if title:
                programme_obj = models.Programme.objects.create(title=title, user=request.user)
            if programme_obj:
                for i in intervals:
                    k = models.IntervalTime.objects.filter(interval=i).first()
                    programme_obj.interval.add(k)
            ret["status"] = True
            ret["msg"] = "成功新建节目！"
        except Exception as e:
            ret["msg"] = "新建节目单失败！"
        return JsonResponse(ret)
    # 取属于该用户的所有时间段
    user = request.user
    user_intervals = user.intervaltime_set.all()
    k = []
    for p in models.Programme.objects.filter(user=user):
        intervals = p.interval.all()
        for i in intervals:
            k.append(i)
    intervals = []
    for m in user_intervals:
        if m not in k:
            intervals.append(m)
    ret = {
        "intervals": intervals
    }
    return render(request, 'show_admin/programme_add.html', ret)



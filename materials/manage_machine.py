from materials import models
from django.shortcuts import render


def manage_machine(request):
    # TODO 查询每个用户下的设备
    users = models.UserInfo.objects.all()
    manage = {}
    for user in users:
        machines = (models.UserInfo.objects.get(username=user.username)).machine_set.all()
        manage[user] = machines
    ret = {
        'manage': manage,
    }
    return render(request, 'manage_machine.html', ret)

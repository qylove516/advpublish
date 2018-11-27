from materials import models
from django.shortcuts import render
from django.http import JsonResponse


def admin_role(request):
    ret = {

    }
    return render(request, "xadmin/admin_role.html", ret)

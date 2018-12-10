from materials import models
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from materials.get_pgs import get_pg


def admin_role(request):
    # 角色分组
    groups_all = models.Group.objects.all().order_by("name")
    groups, current_page = get_pg(request, groups_all, 8)
    ret = {
        "groups_all": groups_all,
        "groups": groups,
        "current_page": current_page
    }
    return render(request, "xadmin/admin_role.html", ret)


def groups_add(request):
    if request.method == 'POST':
        name = request.POST.get("title")
        ret = {"status": True, "msg": "添加分组成功！"}
        try:
            models.Group.objects.create(name=name)
        except Exception as e:
            ret["msg"] = "添加分组失败！"
        return JsonResponse(ret)
    groups = models.Group.objects.all()
    ret = {
        "groups": groups
    }
    return render(request, 'xadmin/groups_add.html', ret)


def groups_del(request):
    """
    TODO 删除分组 待测试
    """
    pk = request.GET.get("pk")
    ret = {"status": True, "msg": "删除成功"}
    try:
        group = models.Group.objects.filter(pk=pk).first()
        users = group.user_set.all()
        for user in users:
            user.filetag_set.all().delete()  # 删除用户下的标签
            user.materialfiles_set.all().delete()  # 删除用户所有标签下的素材
            programmes = user.programme_set.all()  # 删除每有节目单下的临时素材
            for p in programmes:
                p.programmematerial_set.all().delete()
            programmes.delete()
            # 区域时间更新
            user.areaintervaltime_set.all().update(user=None, is_selected=False, is_inuse=True)
            user.delete()  # 删除用户
        group.delete()
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def groups_update(request, pk):
    if request.method == 'POST':
        name = request.POST.get("title")
        ret = {"status": True, "msg": "修改分组名称成功！"}
        try:
            models.Group.objects.filter(pk=pk).update(name=name)
        except Exception as e:
            ret["msg"] = "添加分组失败！"
        return JsonResponse(ret)
    group = models.Group.objects.filter(pk=pk).first()
    ret = {
        "pk": pk,
        "group": group
    }
    return render(request, 'xadmin/groups_update.html', ret)


def groups_user_add(request, group_pk):
    # 把用户添加到分组中
    if request.method == "POST":
        user_pk = request.POST.get("user_pk")
        ret = {"status": True, "msg": "添加成功！"}
        try:
            models.UserInfo.objects.filter(pk=user_pk).first().groups.add(models.Group.objects.filter(pk=group_pk).first())
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "添加失败！"
        return JsonResponse(ret)
    user_exist = models.Group.objects.filter(pk=group_pk).first().user_set.all()
    user_select = models.UserInfo.objects.filter(Q(is_manage=False) & Q(is_superuser=False))
    users = [i for i in user_select if i not in user_exist]
    ret = {
        "group_pk": group_pk,
        "user_exist": user_exist,
        "users": users
    }
    return render(request, "xadmin/groups_user_add.html", ret)


def groups_user_del(request, group_pk):
    user_pk = request.GET.get("user_pk")
    ret = {"status": True, "msg": "删除成功！"}
    try:
        if user_pk:
            group = models.Group.objects.filter(pk=group_pk).first()
            user = models.UserInfo.objects.filter(pk=user_pk)
            user.update(is_manage=False)
            user.first().groups.remove(group)
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def admin_list(request):
    # 每一个组中只有一个 manage， 在权限管理的时间限制
    user = request.user
    if user.is_manage:
        group = user.groups.all()[0]
        users_all = group.user_set.filter(~Q(pk=user.pk)).order_by("create_time")
        msg = "有审核批准发布节目的权限！"
    elif user.is_superuser:
        users_all = models.UserInfo.objects.all().filter(~Q(pk=user.pk)).order_by("username")
        msg = "有所有的权限！"
        group = "不属于任何组"
    else:
        users_all = None
        msg = None
        group = None
    users, current_page = get_pg(request, users_all, 8)
    ret = {
        "users_all": users_all,
        "users": users,
        "msg": msg,
        "group": group
    }
    return render(request, 'xadmin/admin_list.html', ret)


def user_update(request, user_pk):
    if request.method == "POST":
        ret = {"status": True, "msg": "修改成功！"}
        try:
            username = request.POST.get('username')
            company = request.POST.get("company")
            tel = request.POST.get("tel")
            address = request.POST.get("address")
            email = request.POST.get("email")
            models.UserInfo.objects.filter(pk=user_pk).update(
                username=username,
                company=company,
                tel=tel,
                address=address,
                email=email,
            )
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "修改失败！"
        return JsonResponse(ret)
    user = models.UserInfo.objects.filter(pk=user_pk).first()
    ret = {
        'user_pk': user_pk,
        'username': user.username,
        'company': user.company,
        'tel': user.tel,
        'address': user.address,
        'email': user.email,
    }
    return render(request, "xadmin/user_update.html", ret)


def user_del(request):
    user_pk = request.GET.get("user_pk")
    ret = {"status": True, "msg": "删除成功！"}
    try:
        user = models.UserInfo.objects.filter(pk=user_pk).first()
        user.filetag_set.all().delete()  # 删除用户下的标签
        user.materialfiles_set.all().delete()  # 删除用户所有标签下的素材
        programmes = user.programme_set.all()  # 删除每有节目单下的临时素材
        for p in programmes:
            p.programmematerial_set.all().delete()
        programmes.delete()
        # 区域时间更新
        user.areaintervaltime_set.all().update(user=None, is_selected=False, is_inuse=True)
        user.delete()  # 删除用户
    except Exception as e:
        ret["status"] = False
        ret["msg"] = "删除失败！"
    return JsonResponse(ret)


def user_power_update(request, user_pk):
    if request.method == "POST":
        is_manage = request.POST.get("is_manage")
        if is_manage == "false":
            is_manage = False
        else:
            is_manage = True
        ret = {"status": True, "msg": "修改成功！"}
        try:
            if is_manage:
                user = models.UserInfo.objects.filter(pk=user_pk).first()
                groups = user.groups.all()
                if len(groups) > 1:
                    ret["status"] = False
                    ret["msg"] = "所在组的一级管理员个数大于1，不能提交为一级管理员"
                elif len(groups) == 1:
                    user = groups[0].user_set.filter(~Q(pk=user_pk))
                    user = user.filter(is_manage=True)
                    if len(user) > 0:
                        ret["status"] = False
                        ret["msg"] = "所在组已经有一级管理员，请确认后去除原管理员的权限再更改"
                    else:
                        models.UserInfo.objects.filter(pk=user_pk).update(is_manage=is_manage)
                elif len(groups) == 0:
                    ret["status"] = False
                    ret["msg"] = "此用户暂不在任何分组，请先分组！"
                else:
                    models.UserInfo.objects.filter(pk=user_pk).update(is_manage=is_manage)
            else:
                models.UserInfo.objects.filter(pk=user_pk).update(is_manage=is_manage)

        except Exception as e:
            ret["status"] = False
            ret["msg"] = "修改失败！"
        return JsonResponse(ret)
    user = models.UserInfo.objects.filter(pk=user_pk).first()
    ret = {
        "user_pk": user_pk,
        'is_manage': user.is_manage,
    }
    return render(request, "xadmin/user_power_update.html", ret)

from materials import models
from materials.utils.get_pgs import get_pg
from django.db.models import Q


def programme_related(pk, role):
    programme = None
    if role == "adv":
        programme = models.AdvProgramme.objects.filter(pk=pk).first()
    elif role == "welfare_primary":
        programme = models.PrimaryWelfareProgramme.objects.filter(pk=pk).first()
    elif role == "welfare_secondary":
        programme = models.SecondaryWelfareProgramme.objects.filter(pk=pk).first()
    elif role == "qrcode":
        programme = models.QrCodeProgramme.objects.filter(pk=pk).first()
    elif role == "template":
        programme = models.MachineTemplate.objects.filter(pk=pk).first()
    return programme


# 节目单查看、增加、删除
class Programme(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model
        self.user = self.request.user

    def detail(self, role):
        if self.user.is_superuser:
            programmes = self.model.all()
        else:
            if role == "adv":
                if self.user.is_manage:
                    group = self.user.groups.all()[0]
                    users = group.user_set.all()
                    programmes = []
                    for user in users:
                        for p in self.model.all().filter(user=user):
                            programmes.append(p)
                else:
                    programmes = self.model.filter(user=self.user)
            else:
                if self.user.is_manage:
                    programmes = self.model.filter(user=self.user)
                else:
                    programmes = None
        ret = {
            "programmes": programmes,
            "user_pk": self.user.pk,
        }
        return ret

    def add(self):
        ret = {"status": True, "msg": "创建节目单成功！"}
        title = self.request.POST.get("title")
        try:
            if title:
                self.model.create(title=title, user_id=self.user.pk)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "新建节目单失败！"
        return ret

    def delete(self):
        ret = {"status": True}
        try:
            programme_pk = self.request.GET.get("programme_pk")
            self.model.filter(pk=programme_pk).delete()
        except Exception as e:
            ret["status"] = False
        return ret


class ProgrammeMaterial(object):

    def __init__(self, request, model):
        self.request = request
        self.model = model
        self.user = self.request.user

    def editor(self, programme_pk, role):
        if self.request.method == "POST":
            sort_list = self.request.POST.getlist("sort_list")[0]
            sort_list = sort_list.split(",")
            ret = {"status": True}
            try:
                for s in sort_list:
                    self.model.filter(id=int(s)).update(nid=sort_list.index(s))
            except Exception as e:
                ret["status"] = False
            return ret
        ret = {
            "programme_pk": programme_pk,
            "user_pk": self.user.pk,
        }
        programmes = programme_related(programme_pk, role)
        user = models.UserInfo.objects.filter(pk=self.user.pk).first()
        files = models.MaterialFiles.objects.filter(user=user).order_by("-create_time")
        files, current_page = get_pg(self.request, files, 8)
        if programmes:
            ret["programme_materials"] = self.model.filter(programme_id=programme_pk).order_by("nid")
            ret["programmes"] = programmes
            ret["files"] = files
            ret["current_page"] = current_page
            ret["is_play_time"] = True
        return ret

    def add(self, programme_pk, role):
        if self.request.method == "POST":
            materials = self.request.POST.getlist("materials")[0]
            materials = materials.split(",")
            m_length = len(materials)
            programme = programme_related(programme_pk, role)
            materials_exist = self.model.filter(programme_id=programme_pk)
            ret = {
                "status": True,
                "msg": "添加素材成功！"
            }
            for k in materials_exist:
                nid = k.nid
                k.nid = nid + m_length
                k.save()
            try:
                for p, m in enumerate(materials):
                    material = models.MaterialFiles.objects.filter(pk=m).first()
                    print(material)
                    self.model.create(material=material, programme=programme, nid=p)
            except Exception as e:
                ret["status"] = False
                ret["msg"] = "添加素材失败！"
            return ret

    def delete(self):
        material_pk = self.request.GET.get("material_pk")
        programme_pk = self.request.GET.get("programme_pk")
        material_nid = self.model.filter(pk=material_pk).first().nid
        p_materials = self.model.filter(Q(programme_id=programme_pk), Q(nid__gt=material_nid))
        ret = {
            "status": True,
            "msg": "删除素材成功"
        }
        for k in p_materials:
            nid = k.nid
            k.nid = nid - 1
            k.save()
        try:
            self.model.filter(pk=material_pk).delete()
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "删除素材失败！"
        return ret

    def change_time(self):
        material_related_pk = self.request.GET.get("material_related_pk")
        play_time = self.request.GET.get("play_time")
        ret = {"status": True, "msg": "修改成功！"}
        try:
            self.model.filter(pk=material_related_pk).update(play_time=play_time)
        except Exception as e:
            ret["status"] = False
            ret["msg"] = "修改失败！"
        return ret

    def programme_view(self, programme_pk, role):
        programme = programme_related(programme_pk, role)
        programme_materials = self.model.filter(programme_id=programme_pk)
        ret = {
            "is_play_time": True,
            "programme": programme,
            "programme_materials": programme_materials
        }
        return ret

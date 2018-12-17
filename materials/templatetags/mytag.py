from django import template
from materials import models

register = template.Library()

img = ["bmp", "jpg", "jpeg", "png"]


# 识别上传文件的格式
@register.filter
def image_video(url):
    style = url.split(".")
    if style[-1] in img:
        return True
    return False


@register.filter
def list_length(li):
    k = len(li)
    return k


@register.filter
def is_power(request_pk, user_pk):
    if request_pk == user_pk:
        return True
    else:
        return False


@register.filter
def is_user_manage(pk):
    user = models.UserInfo.objects.filter(pk=pk).first()
    if not user.is_manage and not user.is_superuser:
        return True
    else:
        return False


@register.filter
def area_list(area_pk):
    area = models.Area.objects.filter(pk=area_pk).first()

    machines = area.machine_set.all().values('nid', 'title')
    if len(machines) > 0:
        return machines


@register.filter
def machine_to_interval(pk):
    intervals = models.AdvProgrammeRelated.objects.filter(pk=pk).first().interval.all()
    return intervals


@register.filter
def compare_interval(interval_pk, interval_list):
    if interval_pk in interval_list:
        return True
    else:
        return False

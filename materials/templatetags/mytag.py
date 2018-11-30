from django import template
from materials import models
from django.db.models import Q

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
    if not user.is_superuser and not user.is_superuser:
        return True
    else:
        return False

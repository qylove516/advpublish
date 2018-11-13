from django import template

register = template.Library()

img = ["bmp", "jpg", "jpeg", "png"]


# 识别上传文件的格式
@register.filter
def image_video(url):
    style = url.split(".")
    if style[-1] in img:
        return True
    return False

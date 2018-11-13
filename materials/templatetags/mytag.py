from django import template

register = template.Library()

img = ["bmp", "jpg", "jpeg", "png"]


@register.filter
def image_video(url):
    print(url)
    style = url.split(".")
    if style[-1] in img:
        return True
    return False

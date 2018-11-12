from django.contrib import admin
from materials import models
# Register your models here.


admin.site.register(models.UserInfo)
admin.site.register(models.IntervalTime)
admin.site.register(models.Material)
admin.site.register(models.Machine)
admin.site.register(models.Programme)
admin.site.register(models.Tag)
admin.site.register(models.MaterialFiles)
admin.site.register(models.FileTag)

from django.contrib import admin
from materials import models
# Register your models here.


admin.site.register(models.UserInfo)
admin.site.register(models.Machine)
admin.site.register(models.Area)
admin.site.register(models.MaterialFiles)
admin.site.register(models.FileTag)

# 广告节目
admin.site.register(models.AdvProgramme)
admin.site.register(models.AdvProgrammeMaterial)
admin.site.register(models.AdvProgrammeRelated)
# 公益节目主屏
admin.site.register(models.PrimaryWelfareProgramme)
admin.site.register(models.PrimaryWelfareProgrammeMaterial)
admin.site.register(models.PrimaryProgrammeRelated)
# 公益节目副屏
admin.site.register(models.SecondaryWelfareProgramme)
admin.site.register(models.SecondaryWelfareProgrammeMaterial)
admin.site.register(models.SecondaryWelfareProgrammeRelated)


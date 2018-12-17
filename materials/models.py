from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from materials.apps import time_choices


class UserInfo(AbstractUser):
    company = models.CharField("单位/公司", max_length=256, blank=True, null=True)
    tel = models.CharField("联系方式", max_length=11, blank=True, null=True)
    address = models.CharField("联系地址", max_length=256, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    is_manage = models.BooleanField("管理员", default=False)

    @property
    def groups_all(self):
        gps = self.groups.all()
        gp_name = []
        for gp in gps:
            gp_name.append(gp.name)
        return ",".join(gp_name)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Area(models.Model):
    # 区域标题唯一
    title = models.CharField("标题", max_length=64, unique=True)
    is_selected = models.BooleanField("是否已选择", default=False)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "设备区域"
        verbose_name_plural = "设备区域"


class Machine(models.Model):
    title = models.CharField("名称", max_length=64)
    nid = models.CharField(primary_key=True, max_length=256)
    position = models.CharField("地理位置", max_length=256, blank=True, null=True)
    supplier = models.CharField("供应商", max_length=62, blank=True, null=True)
    heart_time = models.DateTimeField("心跳时间", blank=True, null=True)
    update_time = models.DateTimeField("更新时间", blank=True, null=True)
    area = models.ForeignKey(
        Area,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备"


class FileTag(models.Model):
    title = models.CharField("标签", max_length=64)
    user = models.ForeignKey(
        to='UserInfo',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文件标签"
        verbose_name_plural = "文件标签"


class MaterialFiles(models.Model):
    title = models.CharField("标题", max_length=32, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to="UserInfo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    files = models.FileField("文件", upload_to="documents/")
    tag = models.ForeignKey(
        FileTag,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件"


class IntervalTime(models.Model):
    title = models.CharField("时间段", max_length=32, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "时间段"
        verbose_name_plural = "时间段"


class Programme(models.Model):
    # TODO title 设置为unique
    title = models.CharField('标题', max_length=64)
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        UserInfo,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class ProgrammeMaterial(models.Model):
    # TODO 把 material blank=True null=True 去掉
    nid = models.IntegerField("序号", blank=True, null=True)
    material = models.ForeignKey(
        to="MaterialFiles",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.material:
            return self.material.title
        return self.nid

    class Meta:
        abstract = True


class AdvProgramme(Programme):

    class Meta:
        verbose_name = "广告节目"
        verbose_name_plural = "广告节目"


class AdvProgrammeMaterial(ProgrammeMaterial):
    """广告节目素材"""
    programme = models.ForeignKey(
        AdvProgramme,
        blank=True,
        null=True,
        on_delete=models.CASCADE  # 删除节目表，同时此素材临时表也会删除
    )
    play_time = models.PositiveIntegerField("播放时间", default=10, help_text="单位/秒")

    class Meta:
        verbose_name = "广告节目素材"
        verbose_name_plural = "广告节目素材"


class AdvProgrammeRelated(models.Model):
    """ 广告节目关联设备时间"""
    title = models.CharField("标题", max_length=64, blank=True, null=True)
    is_review = models.BooleanField("是否提交审核", default=False)
    is_publish = models.BooleanField("是否发布", default=False)
    interval = models.ManyToManyField(
        IntervalTime,
        blank=True,
    )
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )
    programme = models.ForeignKey(
        AdvProgramme,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "广告节目关联设备时间"
        verbose_name_plural = "广告节目关联设备时间"
        unique_together = ('machine', 'programme',)


class PrimaryWelfareProgramme(Programme):
    """公益节目主屏"""

    class Meta:
        verbose_name = "公益节目主屏"
        verbose_name_plural = "公益节目主屏"


class PrimaryWelfareProgrammeMaterial(ProgrammeMaterial):
    """公益节目主屏素材"""
    programme = models.ForeignKey(
        PrimaryWelfareProgramme,
        blank=True,
        null=True,
        on_delete=models.CASCADE  # 删除节目表，同时此素材临时表也会删除
    )
    play_time = models.PositiveIntegerField("播放时间", default=10, help_text="单位/秒")

    class Meta:
        verbose_name = "公益节目主屏素材"
        verbose_name_plural = "公益节目主屏素材"


class PrimaryWelfareProgrammeRelated(models.Model):
    """公益节目主屏关联设备"""
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )
    programme = models.ForeignKey(
        PrimaryWelfareProgramme,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.machine.title + self.programme.title

    class Meta:
        verbose_name = "公益节目主屏关联设备"
        verbose_name_plural = "公益节目主屏关联设备"
        unique_together = ("programme", "machine")


class SecondaryWelfareProgramme(Programme):
    class Meta:
        verbose_name = "公益节目副屏"
        verbose_name_plural = "公益节目副屏"


class SecondaryWelfareProgrammeMaterial(ProgrammeMaterial):
    programme = models.ForeignKey(
        SecondaryWelfareProgramme,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "公益节目副屏素材"
        verbose_name_plural = "公益节目副屏素材"


class SecondaryWelfareProgrammeRelated(models.Model):
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE
    )
    welfare_programme = models.ForeignKey(
        SecondaryWelfareProgramme,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.machine.title + "--" + self.welfare_programme.title

    class Meta:
        verbose_name = "公益节目副屏关联设备"
        verbose_name_plural = "公益节目副屏关联设备"
        unique_together = ("machine", "welfare_programme")

from django.db import models
from django.contrib.auth.models import auth, AbstractUser, Group


class UserInfo(AbstractUser):
    company = models.CharField("单位/公司", max_length=256, blank=True, null=True)
    tel = models.CharField("联系方式", max_length=11, blank=True, null=True)
    address = models.CharField("联系地址", max_length=256, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)
    is_manage = models.BooleanField("管理员", default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class IntervalTime(models.Model):
    # 时间段标题唯一
    interval = models.CharField("时间段", max_length=32, unique=True)
    user = models.ForeignKey(
        to="UserInfo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.interval

    class Meta:
        verbose_name = "时间段"
        verbose_name_plural = "时间段"


class Area(models.Model):
    # 区域标题唯一
    title = models.CharField("标题", max_length=64, unique=True)
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


class AreaIntervalTime(models.Model):
    # 在一个时间段，一个区域，只能选择一个节目单
    interval_time = models.ForeignKey(
        IntervalTime,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    area = models.ForeignKey(
        Area,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        UserInfo,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    programme = models.ForeignKey(
        to="Programme",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    is_selected = models.BooleanField(default=False)
    is_inuse = models.BooleanField(default=False)

    def __str__(self):
        return "{area}-{time}".format(area=self.area.title, time=self.interval_time.interval)

    class Meta:
        verbose_name = "区域时间"
        verbose_name_plural = "区域时间"


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
        on_delete=models.SET_NULL
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


class Programme(models.Model):
    title = models.CharField('标题', max_length=64)
    is_review = models.BooleanField("是否提交审核", default=False)
    is_publish = models.BooleanField("是否发布", default=False)
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to="UserInfo",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "节目单"
        verbose_name_plural = "节目单"


class ProgrammeMaterial(models.Model):
    # 每一个节目单对应多个素材，先创建节目单，再在节目单中添加素材
    nid = models.PositiveIntegerField("序号", blank=True, null=True)
    programme = models.ForeignKey(
        to="Programme",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    material = models.ForeignKey(
        to="MaterialFiles",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        if self.material:
            return self.material.title
        return self.nid

    class Meta:
        verbose_name = "节目单素材"
        verbose_name_plural = "节目单素材"

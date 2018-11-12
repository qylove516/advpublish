from django.db import models
from django.contrib.auth.models import auth, AbstractUser


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    company = models.CharField("单位/公司", max_length=256, blank=True, null=True)
    tel = models.CharField("联系方式", max_length=11, blank=True, null=True)
    address = models.CharField("联系地址", max_length=256, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"


class Machine(models.Model):
    nid = models.CharField(primary_key=True, max_length=256)
    position = models.CharField("地理位置", max_length=256, blank=True, null=True)
    supplier = models.CharField("供应商", max_length=62, blank=True, null=True)
    heart_time = models.DateTimeField("心跳时间", blank=True, null=True)
    user = models.ManyToManyField(
        to="UserInfo",
        blank=True
    )

    def __str__(self):
        return self.nid

    class Meta:
        verbose_name = "设备"
        verbose_name_plural = "设备"


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField("标签", max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"


class MaterialFather(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField("标题", max_length=32, blank=True, null=True)
    tag = models.ForeignKey(
        Tag,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    create_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        to="UserInfo",
        to_field="nid",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Material(MaterialFather):
    files = models.ImageField("图片", upload_to="")

    class Meta:
        verbose_name = "图片"
        verbose_name_plural = "图片"


class MaterialFiles(MaterialFather):
    files = models.FileField("文件", upload_to="documents/")

    class Meta:
        verbose_name = "文件"
        verbose_name_plural = "文件"


class IntervalTime(models.Model):
    nid = models.AutoField(primary_key=True)
    interval = models.CharField("时间段", max_length=32)
    user = models.ForeignKey(
        to="UserInfo",
        to_field="nid",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.interval

    class Meta:
        verbose_name = "时间段"
        verbose_name_plural = "时间段"


class Programme(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField('标题', max_length=64)
    is_publish = models.BooleanField("是否发布", default=False)
    create_time = models.DateTimeField(auto_now=True)
    files = models.ManyToManyField(
        to="Material",
        blank=True,
    )

    interval = models.ForeignKey(
        to="IntervalTime",
        to_field="nid",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    machine = models.ManyToManyField(
        to="Machine",
        blank=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "节目单"
        verbose_name_plural = "节目单"

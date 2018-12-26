from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin
from materials import models
from materials.serializers import adv, welfare, qrcode, template


# 、公益节目主屏、公益节目副屏、二维码、背景模板
class AdvProgrammeAPIViews(ViewSetMixin, APIView):
    """广告节目"""

    def adv_list(self, request, *args, **kwargs):
        """
        获取广告节目
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        nid = kwargs.get("nid")
        # 广告节目单列表
        queryset = models.AdvProgramme.objects.filter(advprogrammerelated__machine__nid=nid)
        adv_programme = adv.AdvProgrammeSerializers(instance=queryset, many=True)
        return Response(adv_programme.data)


class WelfarePrimaryProgrammeAPIView(ViewSetMixin, APIView):
    """公益主屏"""

    def welfare_primary_list(self, request, *args, **kwargs):
        """
        获取公益主屏节目单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        nid = kwargs.get("nid")
        # 公益主屏节目单列表
        queryset = models.PrimaryWelfareProgramme.objects.filter(primarywelfareprogrammerelated__machine__nid=nid).first()
        welfare_primary_programme = welfare.WelfarePrimaryProgrammeSerializers(instance=queryset, many=False)
        return Response(welfare_primary_programme.data)


class WelfareSecondaryProgrammeAPIView(ViewSetMixin, APIView):
    """公益副屏"""

    def welfare_secondary_list(self, request, *args, **kwargs):
        """
        获取公益副屏节目单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        nid = kwargs.get("nid")
        # 公益副屏节目单列表
        queryset = models.SecondaryWelfareProgramme.objects.filter(secondarywelfareprogrammerelated__machine__nid=nid).first()
        welfare_secondary_programme = welfare.WelfareSecondaryProgrammeSerializers(instance=queryset, many=False)
        return Response(welfare_secondary_programme.data)


class QrCodeProgrammeAPIView(ViewSetMixin, APIView):
    """二维码"""

    def qr_code_list(self, request, *args, **kwargs):
        """
        获取二维码节目单
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        nid = kwargs.get("nid")
        # 二维码节目单列表
        queryset = models.QrCodeProgramme.objects.filter(qrcodeprogrammerelated__machine__nid=nid).first()
        qr_code_programme = qrcode.QrCodeProgrammeSerializers(instance=queryset, many=False)
        return Response(qr_code_programme.data)


class TemplateProgrammeAPIView(ViewSetMixin, APIView):
    """背景"""

    def template_list(self, request, *args, **kwargs):
        """
        背景
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        nid = kwargs.get("nid")
        # 背景节目单列表
        queryset = models.MachineTemplate.objects.filter(machinetemplaterelated__machine__nid=nid).first()
        template_programme = template.TemplateProgrammeSerializers(instance=queryset, many=False)
        return Response(template_programme.data)

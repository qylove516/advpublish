from materials.utils.file_md5 import get_md5
from rest_framework import serializers
from materials import models


class QrCodeProgrammeSerializers(serializers.ModelSerializer):
    """
    二维码节目素材
    """
    materials = serializers.SerializerMethodField()

    def get_materials(self, obj):
        # 二维码节目单关联素材
        materials_related = obj.qrcodeprogrammematerial_set.all()
        materials = [{'title_md5': get_md5(material.material.files.url.split('/')[-1]), 'file': material.material.files.url} for material in materials_related]
        return materials

    class Meta:
        model = models.QrCodeProgramme
        fields = ('materials', )

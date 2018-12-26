from materials.utils.file_md5 import get_md5
from rest_framework import serializers
from materials import models


class WelfarePrimaryProgrammeSerializers(serializers.ModelSerializer):
    """
    主屏节目素材
    """
    materials = serializers.SerializerMethodField()

    def get_materials(self, obj):
        # 节目单关联素材
        materials_related = obj.primarywelfareprogrammematerial_set.all()
        materials = [{'title_md5': get_md5(material.material.files.url.split('/')[-1]), 'file': material.material.files.url, 'play_time': material.play_time} for material in materials_related]
        return materials

    class Meta:
        model = models.PrimaryWelfareProgramme
        fields = ('materials', )


class WelfareSecondaryProgrammeSerializers(serializers.ModelSerializer):
    """
    副屏节目素材
    """
    materials = serializers.SerializerMethodField()

    @staticmethod
    def get_materials(obj):
        # 节目单关联素材
        materials_related = obj.secondarywelfareprogrammematerial_set.all()
        materials = [{'title_md5': get_md5(material.material.files.url.split('/')[-1]), 'file': material.material.files.url} for material in materials_related]
        return materials

    class Meta:
        model = models.SecondaryWelfareProgramme
        fields = ('materials', )

from materials.utils.file_md5 import get_md5
from rest_framework import serializers
from materials import models


class AdvProgrammeSerializers(serializers.ModelSerializer):
    """
    广告节目素材
    """
    materials = serializers.SerializerMethodField()
    intervals = serializers.SerializerMethodField()

    def get_materials(self, obj):
        # 节目单关联素材
        materials_related = obj.advprogrammematerial_set.all()
        materials = [{'title_md5': get_md5(material.material.files.url.split('/')[-1]), 'file': material.material.files.url, 'play_time': material.play_time} for material in materials_related]
        return materials

    def get_intervals(self, obj):
        # 节目单关联列表
        programme_related = obj.advprogrammerelated_set.all()[0]
        # 节目单关联列表关联时间
        intervals_related = programme_related.interval.all()
        intervals = [interval.title for interval in intervals_related]
        return intervals

    class Meta:
        model = models.AdvProgramme
        fields = ('materials', 'intervals')

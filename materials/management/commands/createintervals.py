from django.core.management.base import BaseCommand, CommandError
from materials import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        hour_list = ["{num:02d}".format(num=i) + ':00-' + '{k:02d}'.format(k=i + 1) + ':00' for i in range(24)]
        try:
            for h in hour_list:
                if h == "23:00-24:00":
                    models.IntervalTime.objects.create(interval="23:00-00:00")
                else:
                    models.IntervalTime.objects.create(interval=h)
            print("成功插入数据！")
        except Exception as e:
            raise CommandError("插入数据失败！ %s" % e)

# Generated by Django 2.1.3 on 2018-12-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20181212_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advprogrammematerial',
            name='nid',
            field=models.IntegerField(blank=True, null=True, verbose_name='序号'),
        ),
        migrations.AlterField(
            model_name='primarywelfareprogrammematerial',
            name='nid',
            field=models.IntegerField(blank=True, null=True, verbose_name='序号'),
        ),
        migrations.AlterField(
            model_name='secondarywelfareprogrammematerial',
            name='nid',
            field=models.IntegerField(blank=True, null=True, verbose_name='序号'),
        ),
    ]

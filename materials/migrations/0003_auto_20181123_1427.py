# Generated by Django 2.1.3 on 2018-11-23 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20181123_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetag',
            name='title',
            field=models.CharField(max_length=64, verbose_name='标签'),
        ),
    ]

# Generated by Django 2.1.3 on 2018-11-23 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_auto_20181123_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='title',
            field=models.CharField(max_length=64, verbose_name='名称'),
        ),
    ]

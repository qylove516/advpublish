# Generated by Django 2.1.3 on 2018-12-07 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_auto_20181207_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='advprogrammerelated',
            name='title',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='标题'),
        ),
    ]
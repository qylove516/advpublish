# Generated by Django 2.1.3 on 2018-12-12 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advprogramme',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='primarywelfareprogramme',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='primarywelfareprogrammematerial',
            name='play_time',
        ),
        migrations.RemoveField(
            model_name='secondarywelfareprogramme',
            name='is_public',
        ),
        migrations.RemoveField(
            model_name='secondarywelfareprogrammematerial',
            name='play_time',
        ),
    ]
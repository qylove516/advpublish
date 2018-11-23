# Generated by Django 2.1.3 on 2018-11-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='areaintervaltime',
            name='is_blank',
        ),
        migrations.AddField(
            model_name='areaintervaltime',
            name='is_inuse',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='areaintervaltime',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
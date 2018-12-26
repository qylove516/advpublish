from django.urls import path, re_path
from materials.views import views
from materials.views import assign, adv_programme, area_machines, xadmin, welfare_programme, qrcode

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),

    path('areas/get_areas/', area_machines.areas_get, name='areas'),
    path('areas/areas_add/', area_machines.areas_add, name='areas_add'),
    path('areas/areas_del/', area_machines.areas_del, name='areas_del'),
    re_path(r'^areas/areas_update/(\d*)/$', area_machines.areas_update, name='areas_update'),

    path('machine/machine_related_del/', area_machines.machine_related_del, name='machine_related_del'),
    path('machine/machine_related_publish/', area_machines.machine_related_publish, name="machine_related_publish"),
    re_path(r'^machines/machine_detail/(\d*)/$', area_machines.machine_detail, name='machine_detail'),
    re_path(r'^machines/machine_update/(\d*)/$', area_machines.machine_update, name='machine_update'),
    re_path(r'^machines/(\d*)/$', area_machines.machine_list, name='machine_list'),
    re_path(r'^machines/machines_add/(\d*)/$', area_machines.machines_add, name='machines_add'),
    re_path(r'^machines/machine_addpi/(\d*)/$', area_machines.machine_addpi, name='machine_addpi'),
    path('tags/', views.tags, name='tags'),
    re_path(r'^tags_update/(\d*)/$', views.tags_update, name='tags_update'),
    path('tags/tags_add/', views.tag_add, name='material_tag_add'),
    path('tags/tags_delete/', views.tags_delete, name='tags_delete'),

    path('materials/', views.materials, name='materials'),
    path('materials/material_add/', views.materials_add, name='material_file_add'),
    path('materials/material_delete/', views.materials_delete, name='materials_delete'),

    path('adv_programme/', adv_programme.adv_programme, name='adv_programme'),
    path('adv_programme/adv_programme_del/', adv_programme.adv_programme_del, name='adv_programme_del'),
    path('adv_programme/adv_programme_add/', adv_programme.adv_programme_add, name='adv_programme_add'),
    path('programme/programme_material/del/', adv_programme.adv_programme_material_del, name='adv_programme_material_del'),
    path('programme/programme_change_time/', adv_programme.programme_change_time, name='programme_change_time'),
    re_path(r'^adv_programme/programme_editor/(\d*)/$', adv_programme.adv_programme_editor, name='adv_programme_editor'),
    re_path(r'^adv_programme/programme_material_add/(\d*)/$', adv_programme.adv_programme_material_add, name='adv_programme_material_add'),
    re_path(r'^programme/programme_view/(\d*)/$', adv_programme.programme_view, name='programme_view'),

    # 公益主屏节目与设备   使用   (\d*)  表示数字
    path('welfare_primary_programme/welfare_primary_programme/', welfare_programme.welfare_primary_programme, name='welfare_primary_programme'),
    path('welfare_primary_programme/welfare_primary_programme_add/', welfare_programme.welfare_primary_programme_add, name='welfare_primary_programme_add'),
    path('welfare_primary_programme/welfare_primary_programme_del/', welfare_programme.welfare_primary_programme_del, name='welfare_primary_programme_del'),
    path('welfare_primary_material/welfare_primary_material_del/', welfare_programme.welfare_primary_material_del, name='welfare_primary_material_del'),
    path('welfare_primary_material/welfare_primary_material_change_time/', welfare_programme.welfare_primary_material_change_time, name='welfare_primary_material_change_time'),
    re_path(r'^welfare_primary_material/welfare_primary_material_editor/(\d*)/$', welfare_programme.welfare_primary_programme_editor, name='welfare_primary_programme_editor'),
    re_path(r'^welfare_primary_material/welfare_primary_material_add/(\d*)/$', welfare_programme.welfare_primary_material_add, name="welfare_primary_material_add"),
    re_path(r'^welfare_primary_material/welfare_primary_material_view/(\d*)/$', welfare_programme.welfare_primary_material_view, name='welfare_primary_material_view'),
    # 公益副屏
    path('welfare_secondary_programme/welfare_secondary_programme/', welfare_programme.welfare_secondary_programme, name='welfare_secondary_programme'),
    path('welfare_secondary_programme/welfare_secondary_programme_add/', welfare_programme.welfare_secondary_programme_add, name='welfare_secondary_programme_add'),
    path('welfare_secondary_programme/welfare_secondary_programme_del/', welfare_programme.welfare_secondary_programme_del, name='welfare_secondary_programme_del'),
    path('welfare_secondary_material/welfare_secondary_material_del/', welfare_programme.welfare_secondary_material_del, name='welfare_secondary_material_del'),
    re_path(r'welfare_secondary_material/welfare_secondary_material_editor/(\d*)/$', welfare_programme.welfare_secondary_material_editor, name='welfare_secondary_material_editor'),
    re_path(r'^welfare_secondary_material/welfare_secondary_material_add/(\d*)/$', welfare_programme.welfare_secondary_material_add, name='welfare_secondary_material_add'),
    re_path(r'^welfare_secondary_material/welfare_secondary_material_view/(\d*)/$', welfare_programme.welfare_secondary_material_view, name='welfare_secondary_material_view'),
    # 节目单与设备关联
    re_path(r'^welfare_programme/welfare_programme_machine/(\d*)/$', welfare_programme.welfare_programme_machine, name="welfare_programme_machine"),
    # 设备与模板
    path('template/', qrcode.machine_template, name="machine_template"),
    path('template/machine_template_add/', qrcode.machine_template_add, name="machine_template_add"),
    path('template/machine_template_del/', qrcode.machine_template_del, name="machine_template_del"),
    path('template/machine_material_del/', qrcode.machine_material_del, name='machine_material_del'),
    re_path(r'^template/machine_template_editor/(\d*)/$', qrcode.machine_template_editor, name="machine_template_editor"),
    re_path(r'^template/machine_material_add/(\d*)/$', qrcode.machine_material_add, name="machine_material_add"),
    re_path(r'^tempmlate/machine_material_view/(\d*)/$', qrcode.machine_material_view, name="machine_material_view"),

    # 二维码节目单
    path('qrcode/qrcode_programme/', qrcode.qrcode_programme, name="qrcode_programme"),
    path('qrcode/qrcode_programme_add/', qrcode.qrcode_programme_add, name='qrcode_programme_add'),
    path('qrcode/qrcode_programme_del/', qrcode.qrcode_programme_del, name="qrcode_programme_del"),
    path('qrcode/qrcode_material_del/', qrcode.qrcode_material_del, name="qrcode_material_del"),

    re_path(r'^qrcode/qrcode_programme_editor/(\d*)/$', qrcode.qrcode_programme_editor, name="qrcode_programme_editor"),
    re_path(r'^qrcode/qrcode_material_add/(\d*)/$', qrcode.qrcode_material_add, name="qrcode_material_add"),
    re_path(r'^qrcode/qrcode_material_view/(\d*)/$', qrcode.qrcode_material_view, name="qrcode_material_view"),

    re_path(r'^assign/assign_area/(\w*)/$', assign.assign_area, name='assign_area'),
    re_path(r'^assign/db_area/(\w*)/$', assign.db_area, name='db_area'),

    # 时间分配，后续作用升级使用

    path('xadmin/', xadmin.admin_role, name="admin_role"),
    path('xadmin/admin_list/', xadmin.admin_list, name="admin_list"),
    path('xadmin/user_del/', xadmin.user_del, name="user_del"),
    path('xadmin/groups_add/', xadmin.groups_add, name='groups_add'),
    path('xadmin/groups_del/', xadmin.groups_del, name='groups_del'),
    re_path(r'^xadmin/user_update/(\d*)/$', xadmin.user_update, name='user_update'),
    re_path(r'^xadmin/user_power_update/(\d*)/$', xadmin.user_power_update, name='user_power_update'),
    re_path('xadmin/groups_update/(\d*)/$', xadmin.groups_update, name='groups_update'),
    re_path('xadmin/groups_user_add/(\d*)/$', xadmin.groups_user_add, name='groups_user_add'),
    re_path('xadmin/groups_user_del/(\d*)/$', xadmin.groups_user_del, name='groups_user_del'),
]

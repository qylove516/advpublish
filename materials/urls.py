from django.urls import path, re_path
from materials import views
from materials import assign, programme, area_machines, xadmin

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),

    path('areas/get_areas/', area_machines.areas_get, name='areas'),
    path('areas/areas_add/', area_machines.areas_add, name='areas_add'),
    path('areas/areas_del/', area_machines.areas_del, name='areas_del'),
    re_path(r'^areas/areas_update/(\d*)/$', area_machines.areas_update, name='areas_update'),

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

    path('programme/', programme.adv_programme, name='programme'),
    path('programme/adv_programme_del/', programme.adv_programme_del, name='programme_del'),
    path('programme/adv_programme_add/', programme.adv_programme_add, name='adv_programme_add'),
    path('programme/programme_publish/', programme.programme_publish, name='programme_publish'),
    path('programme/programme_unpublish/', programme.programme_unpublish, name='programme_unpublish'),
    path('programme/programme_material/del/', programme.adv_programme_material_del, name='adv_programme_material_del'),

    re_path(r'^programme/programme_editor/(\d*)/(\d*)/$', programme.adv_programme_editor, name='adv_programme_editor'),
    re_path(r'^programme/programme_material/add/(\d*)/(\d*)/$', programme.adv_programme_material_add,
            name='programme_material_add'),
    # 使用   (\d*)  表示数字

    re_path(r'^assign/assign_area/(\w*)/$', assign.assign_area, name='assign_area'),
    re_path(r'^assign/db_area/(\w*)/$', assign.db_area, name='db_area'),

    # 时间分配，后续作用升级使用
    # re_path(r'^assign/db_time/(\w*)/$', assign.db_time, name='db_time'),
    # re_path(r'^assign/assign_time/(\w*)/(\w*)/$', assign.assign_time, name='assign_time'),

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

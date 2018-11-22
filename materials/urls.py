from django.urls import path, re_path
from materials import views
from materials import manage_machine, programme, machines, intervals
urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),

    path('areas/', machines.areas, name='areas'),
    path('areas/areas_add/', machines.areas_add, name='areas_add'),
    path('areas/areas_del/', machines.areas_del, name='areas_del'),
    re_path(r'^areas/areas_update/(\d*)/$', machines.areas_update, name='areas_update'),


    re_path(r'^machines/machine_detail/(\d*)/$', machines.machine_detail, name='machine_detail'),
    re_path(r'^machines/machine_update/(\d*)/$', machines.machine_update, name='machine_update'),
    re_path(r'^machines/(\d*)/$', machines.machine_area, name='machine_area'),
    re_path(r'^machines/machines_add/(\d*)/$', machines.machines_add, name='machines_add'),

    path('tags/', views.tags, name='tags'),
    re_path(r'^tags_update/(\d*)/$', views.tags_update, name='tags_update'),
    path('tags/tags_add/', views.tag_add, name='material_tag_add'),
    path('tags/tags_delete/', views.tags_delete, name='tags_delete'),

    path('materials/', views.materials, name='materials'),
    path('materials/material_add/', views.materials_add, name='material_file_add'),
    path('materials/material_delete/', views.materials_delete, name='materials_delete'),

    path('programme/', programme.programme, name='programme'),
    path('programme/programme_del/', programme.programme_del, name='programme_del'),
    path('programme/programme_add/', programme.programme_add, name='programme_add'),
    re_path(r'programme/programme_sort/(\d*)/$', programme.programme_sort, name='programme_sort'),
    re_path(r'programme/programme_material_del/(\d*)/$', programme.programme_material_del, name='programme_material_del'),
    re_path(r'^programme/programme_material_add/(\d*)/(\w*)/$', programme.programme_material_add, name='programme_material_add'),

    path('intervals/', intervals.intervals, name='intervals'),
    path('intervals/intervals_add/', intervals.intervals_add, name='intervals_add'),
    path('intervals/intervals_del/', intervals.intervals_del, name='intervals_del'),

    re_path(r'^manage_machine/manage_area/(\w*)/(\w*)/$', manage_machine.manage_area, name='manage_area'),
    re_path(r'^manage_machine/(\w*)/$', manage_machine.manage_machine, name='manage_machine'),
]


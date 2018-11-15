from django.urls import path
from materials import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),

    path('tags/', views.tags, name='tags'),
    path('tags/tags_add/', views.tag_add, name='material_tag_add'),
    path('tags/tags_delete/', views.tags_delete, name='tags_delete'),

    path('materials/', views.materials, name='materials'),
    path('materials/material_add/', views.materials_add, name='material_file_add'),
    path('materials/material_delete/', views.materials_delete, name='materials_delete'),

    path('programme/', views.programme, name='programme'),
    path('programme/programme_add/', views.programme_add, name='programme_add'),

    path('intervals/', views.intervals, name='intervals'),
    path('intervals/intervals_add/', views.intervals_add, name='intervals_add'),
    path('intervals/intervals_del/', views.intervals_del, name='intervals_del'),
    path('user/', views.user, name='user'),

]

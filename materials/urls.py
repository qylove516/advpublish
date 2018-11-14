from django.urls import path
from materials import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),

    path('tags/', views.tags, name='tags'),
    path('tags/tags_add/', views.tags_add, name='tags_add'),
    path('tags/tags_delete/', views.tags_delete, name='tags_delete'),

    path('materials/', views.materials, name='materials'),
    path('materials/material_add/', views.materials_add, name='materials_add'),
    path('materials/material_delete/', views.materials_delete, name='materials_delete'),

    path('programme/', views.programme, name='programme'),
    path('programme/programme_add/', views.programme_add, name='programme_add'),
    path('user/', views.user, name='user'),

]

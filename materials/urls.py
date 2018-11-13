from django.urls import path
from materials import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('material_file/', views.material_file, name='material_file'),

    path('material/material_file_add/', views.material_file_add, name='material_file_add'),
    path('material/material_file_delete/', views.material_file_delete, name='material_file_delete'),
    path('programme/', views.programme, name='programme'),
    path('programme/programme_add/', views.programme_add, name='programme_add'),
    path('user/', views.user, name='user'),

    # path('material/material_add/', views.material_add, name='material_add'),
    # path('material/', views.material, name='material'),
    # path('material/material_delete/', views.material_delete, name='material_delete'),

]

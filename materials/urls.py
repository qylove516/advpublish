from django.urls import path
from materials import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('material/', views.material, name='material'),
    path('material/material_add/', views.material_add, name='material_add'),
    path('material/material_delete/', views.material_delete, name='material_delete'),
    path('programme/', views.programme, name='programme'),
    path('user/', views.user, name='user'),
]

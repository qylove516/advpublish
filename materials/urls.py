from django.urls import path
from materials import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('material/', views.material, name='material'),
    path('material/<str:tag>/upload/', views.upload, name='upload'),
    path('material/<str:tag>/delete/', views.delete, name='delete'),
    path('programme/', views.programme, name='programme'),
    path('user/', views.user, name='user'),
]

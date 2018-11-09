"""advpublish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from materials import urls as materials_urls
from materials import views
from django.views.static import serve
from advpublish import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    re_path('media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    path('register/', views.register, name="register"),
    path('check_username_exist/', views.check_username_exist, name="check_username_exist"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('materials/', include(materials_urls)),
]

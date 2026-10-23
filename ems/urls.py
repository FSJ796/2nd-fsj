"""
URL configuration for ems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from app01 import views                            # views 现在是一个包（views.py 的升级版），depart/user/pretty 是它的三个子文件

urlpatterns = [
    path('admin/', admin.site.urls),
    path('depart/list/', views.depart.depart_list, name='depart_list'),
    path('depart/add/', views.depart.depart_add, name='depart_add'),
    path('depart/edit/<int:nid>/', views.depart.depart_edit, name='depart_edit'),
    path('depart/delete/<int:nid>/', views.depart.depart_delete, name='depart_delete'),
    path('user/add/', views.user.user_add, name='user_add'),
    path('user/list/', views.user.user_list, name='user_list'),
    path('user/<int:nid>/edit/', views.user.user_edit, name='user_edit'),
    path('pretty/add/', views.pretty.pretty_add, name='pretty_add'),
    path('pretty/list/', views.pretty.pretty_list, name='pretty_list'),
    path('pretty/edit/<int:nid>/', views.pretty.pretty_edit, name='pretty_edit'),
    path('pretty/delete/<int:nid>/', views.pretty.pretty_delete, name='pretty_delete'),
]


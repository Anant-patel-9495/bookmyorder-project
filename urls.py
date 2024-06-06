"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from . import views

urlpatterns = [
    path('', views.basepage, name='base_page'),
    path('hotel_menu/', views.hotelmenu, name='hotelmenu'),
    path('login_page/', views.login_page, name='login_page'),
    path('register_page/', views.register_page, name='regestration'),


    path('manager_site/', views.manager_site, name='manager'),
    path('add_dish/', views.add_dish, name='add_dish'),


    path('page1A/', views.page1A, name='page1A'),
    path('page2A/', views.page2A, name='page2A'),
    path('page3A/', views.page3A, name='page3A'),
    path('page3A1/', views.page3A1),

    
    path('user_cart/', views.cart, name='user_cart'),
    path('cook_site/', views.cook_site, name='cook_site'),
    path('user_bill/', views.user_bill, name='userbill'),
    path('top_seller/', views.export_customer_data, name='top_Seller')
    
]
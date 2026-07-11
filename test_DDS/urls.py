"""
URL configuration for test_DDS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from money_moving.views import add_transaction, add_category, main_menu, add_status, add_type, add_subcategory

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_menu', main_menu, name='main_menu'),
    path('add/', add_transaction, name='add_transaction'),
    path('add_category/', add_category, name='add_category'),
    path('add_subcategory/', add_subcategory, name='add_subcategory'),
    path('add_status/', add_status, name='add_status'),
    path('add_typ/', add_type, name='add_type'),
]

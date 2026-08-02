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
from money_moving.views import add_transaction, main_menu, directory, delete, edit, add_item, all_transactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main_menu', main_menu, name='main_menu'),
    path('transactions/', all_transactions, name='all_transactions'),
    path('add/', add_transaction, name='add_transaction'),
    path('directory/', directory, name='directory'),

    # Универсальные действия для справочников и транзакций
    path('delete/<str:model_name>/<int:item_id>/', delete, name='delete_item'),
    path('edit/<str:model_name>/<int:item_id>/', edit, name='edit_item'),
    path('add/<str:model_name>/', add_item, name='add_item')
]

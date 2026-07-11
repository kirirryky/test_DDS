from django.shortcuts import render, redirect
from .forms import TransactionForm, CategoryForm, StatusForm, TypeForm, SubCategoryForm
from .models import MoneyMovement

# Create your views here.

#Меню
def main_menu(request):
    transactions = MoneyMovement.objects.all().order_by('-date')
    return render(request, 'money_moving/main_menu.html', {'transactions': transactions})

#Добавить транзакцию
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = TransactionForm()

    transactions = MoneyMovement.objects.all().order_by('-date')

    return render(request, 'money_moving/add_transaction.html', {'form': form, 'transactions': transactions})

#Добавить категорию
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = CategoryForm()

    return render(request, 'money_moving/add_category.html', {'form': form})

#Добавить подкатегорию
def add_subcategory(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = SubCategoryForm()

    return render(request, 'money_moving/add_subcategory.html', {'form': form})

#Добавить статус
def add_status(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = StatusForm()

    return render(request, 'money_moving/add_status.html', {'form': form})

#Добавить тип
def add_type(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_menu')
    else:
        form = TypeForm()

    return render(request, 'money_moving/add_type.html', {'form': form})
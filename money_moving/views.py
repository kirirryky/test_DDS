from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import TransactionForm
from .models import MoneyMovement, Type, Status, Category, SubCategory
from datetime import date

# Create your views here.

# Словарь безопасности - что можно редактировать, для защиты таблиц типа User
MODEL_MAP = {
    'type': Type,
    'status': Status,
    'category': Category,
    'subcategory': SubCategory,
}

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

@require_POST
@login_required
def add_item(request, model_name):
    ModelClass = MODEL_MAP.get(model_name)
    if not ModelClass:
        messages.error(request, "Неверный тип справочника!")
        return redirect('directory')

    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, "Поле 'Название' обязательно для заполнения!")
        return redirect('directory')

    field_names = [f.name for f in ModelClass._meta.get_fields()] #<-- Получаем список всех полей из модели
    create_kwargs = {'name': name}

    if 'creator' in field_names:
        create_kwargs['creator'] = request.user

    if 'date' in field_names:
        create_kwargs['date'] = date.today()

    if 'comment' in field_names:
        create_kwargs['comment'] = request.POST.get('comment', '').strip()

    if model_name == 'subcategory':
        category_id = request.POST.get('category')
        if category_id:
            create_kwargs['category_id'] = category_id
        else:
            messages.error(request, "Для подкатегории необходимо выбрать родительскую категорию!")
            return redirect('directory')

    try:
        ModelClass.objects.create(**create_kwargs)
        messages.success(request, f"Запись [{name}] успешно создана.")
    except Exception as e:
        messages.error(request, f"Ошибка БД: {e}")

    return redirect('directory')


@require_POST #Только "post" запросы
def delete(request, model_name, item_id):
    ModelClass = MODEL_MAP.get(model_name)
    if not ModelClass:
        messages.error(request, "Выбран неверный тип справочника!")
        return redirect('directory')

    item = get_object_or_404(ModelClass, pk=item_id)
    item_name = str(item)
    item.delete()

    messages.success(request, f"Запись {item_name} успешно удалена.")
    return redirect('directory')

def edit(request, model_name, item_id):
    ModelClass = MODEL_MAP.get(model_name)
    if not ModelClass:
        messages.error(request, "Ошибка, возможно выбранной записи уже не усуществует или у вас нет прав на редактирование!")
        return redirect('directory')
    
    if request.method == "POST":
        item = get_object_or_404(ModelClass, pk=item_id)
        item.name = request.POST.get("name")

        if hasattr(item, 'comment'):
            item.comment = request.POST.get('comment', '')

        # Для связи категории и подкатегории
        if model_name == 'subcategory':
            category_id = request.POST.get('category')
            if category_id:
                item.category_id = category_id

        item.save()
        messages.success(request, f"Запись {item.name} обновлена.")
        return redirect('directory')

    return redirect('directory')

#Справочники
@login_required
def directory(request):

    types = Type.objects.all()
    statuses = Status.objects.all()
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all().select_related('category')

    context = {
        'types': types, 
        'statuses': statuses, 
        'categories': categories, 
        'subcategories': subcategories,
    }
    return render(request, 'money_moving/directory.html', context)
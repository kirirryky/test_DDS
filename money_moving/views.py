from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
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
    'transaction': MoneyMovement,
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

@login_required
def all_transactions(request):
    #Все транзакции с связанными данными
    transactions = MoneyMovement.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).all()

    # === ФИЛЬТРАЦИЯ === 
    # Фильтрация по дате (от)
    date_from = request.GET.get('date_from')
    if date_from:
        transactions = transactions.filter(date__gte = date_from)

    # Фильтрация по дате (до)
    date_to = request.GET.get('date_to')
    if date_to:
        transactions = transactions.filter(date__lte = date_to)

    # Фильтр по статусу
    status_id = request.GET.get('status')
    if status_id:
        transactions = transactions.filter(status_id = status_id)

    # Фильтр по типу
    type_id = request.GET.get('type')
    if type_id:
        transactions = transactions.filter(type_id = type_id)

    # Фильтр по категории
    category_id = request.GET.get('category')
    if category_id:
        transactions = transactions.filter(category_id = category_id)

    # Фильтр по подкатегории
    subcategory_id = request.GET.get('subcategory')
    if subcategory_id:
        transactions = transactions.filter(subcategory_id = subcategory_id)

    # Фильтр по сумме (от)
    amount_from = request.GET.get('amount_from')
    if amount_from:
        transactions = transactions.filter(amount__gte = amount_from)

    # Фильтр по сумме (до)
    amount_to = request.GET.get('amount_to')
    if amount_to:
        transactions = transactions.filter(amount__lte = amount_to)

    # Поиск по комментарию
    search = request.GET.get('search')
    if search:
        transactions = transactions.filter(
            Q(comment__icontains = search) |
            Q(comment__name__icontains = search) |
            Q(subcategory__name__icontains = search)
        )

    # === СОРТИРОВКА ===
    sort_by = request.GET.get('sort', '-date') # по умолчанию

    valid_sort_fields = ['date' , '-date', 'status__name', '-status__name', 
                         'type__name', '-type__name', 'category__name', '-category__name', 
                         'subcategory__name', '-subcategory__name', 'amount', '-amount']

    if sort_by in valid_sort_fields:
        transactions = transactions.order_by(sort_by)
    else:
        transactions = transactions.order_by('-date')

    from django.core.paginator import Paginator
    paginator = Paginator(transactions, 25) #25 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
        'current_sort': sort_by,
        # Сохраняем фильтры
        'current_filters': request.GET.dict(),
    }

    return render(request, 'money_moving/all_transactions.html', context)
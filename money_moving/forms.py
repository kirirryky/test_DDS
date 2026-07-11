from django import forms
from .models import MoneyMovement
from django.utils import timezone
from .models import Category, Status, Type, SubCategory

class TransactionForm(forms.ModelForm):
    date = forms.DateField(
            initial=timezone.now,
            label="Дата транзакции",
            widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        )
    class Meta:
        model = MoneyMovement
        fields = ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']

        #css-классы
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subcategory': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'comment': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Комментарий'})
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Инфраструктура'})}

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: VPN'})}

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Налог'})}

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Пополнение'})}
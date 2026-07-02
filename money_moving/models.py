from django.db import models
from datetime import date

# Create your models here.
class Status(models.Model):
    Name = models.CharField(max_length=100)

class Type(models.Model):
    Name = models.CharField(max_length=100)

class Category(models.Model):
    Name = models.CharField(max_length=200)

class SubCategory(models.Model):
    Name = models.CharField(max_length=200)

class MoneyMovement(models.Model):
    date = models.DateField(default=date.today, verbose_name="Дата транзакции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Комментарий")
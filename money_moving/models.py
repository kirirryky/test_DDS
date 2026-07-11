from django.db import models
from datetime import date

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    def __str__(self):
        return self.name

class MoneyMovement(models.Model):
    date = models.DateField(default=date.today, verbose_name="Дата транзакции")
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Статус")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, verbose_name="Тип")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, verbose_name="Подкатегория")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Комментарий")
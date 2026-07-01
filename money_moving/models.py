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
    date = models.DateField(default=date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=500, blank=True, null=True)
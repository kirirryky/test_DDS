from django.contrib import admin

# Register your models here.
from .models import Status, Type, Category, SubCategory, MoneyMovement

admin.site.register(Status)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(MoneyMovement)

class MoneyMovementAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'type', 'category', 'amount', 'comment')
    list_filter = ('date', 'status', 'type', 'category')
    list_editable = ('date', 'comment')
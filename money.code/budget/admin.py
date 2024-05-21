from django.contrib import admin

# Register your models here.
from .models import BudgetItemRef, Month, BudgetItem, OpElement

admin.site.register(BudgetItemRef)
admin.site.register(Month)
admin.site.register(BudgetItem)
admin.site.register(OpElement)

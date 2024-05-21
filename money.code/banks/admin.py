from django.contrib import admin

# Register your models here.
from .models import Bank, ColorField, ColorWidget, BankAccount, PayMedia, Operation

admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(PayMedia)
admin.site.register(Operation)


class BankAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ColorField: {'widget': ColorWidget }
    }

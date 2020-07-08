from django.contrib import admin

# Register your models here.
from . import models


class Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'image', 'available']
    list_editable = ['name', 'price', 'available']


admin.site.register(models.Product, Admin)
admin.site.register(models.Purchase)
admin.site.register(models.Refund)

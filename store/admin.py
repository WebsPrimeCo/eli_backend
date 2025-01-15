from django.contrib import admin

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'top_product']
    list_editable = ['top_product']
    ordering = ['title', ]

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
    'category',
     'title',
     'slug',
    #  'available_colors',
    #  'available_size',
     'inventory',
     'price'
     ]


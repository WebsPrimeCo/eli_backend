from django.contrib import admin

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'top_product']
    list_editable = ['top_product']
    ordering = ['title', ]
    list_per_page= 10

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('product')

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
    'category',
     'title',
     'slug',
     'inventory',
     'price'
     ]
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('available_colors', 'available_size')

@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', ]

@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = []

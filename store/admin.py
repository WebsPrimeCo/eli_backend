from django.contrib import admin
from django.utils.translation import gettext as _

from . import models

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'top_product']
    list_editable = ['top_product']
    ordering = ['title', ]
    list_per_page= 10
    search_fields = ['title', ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('top_product', 'products')

@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discount', 'description']


    


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
     'title',
    'category',
     'slug',
     'inventory',
     'price',
     ]
    
    list_select_related = ['category']
    actions = ['clear_inventory']
    prepopulated_fields = {
        'slug' : ['title', ]
    }
    search_fields = ['title',]
    autocomplete_fields = ['category',]


    @admin.action(description= _('Out of supply'))
    def clear_inventory(self, request, queryset):
        queryset.update(inventory= 0)

@admin.register(models.Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(models.Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size', ]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'body', 'status', 'rate']
    autocomplete_fields = ['product', 'user']

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone_number', 'city']
    search_fields = ['first_name', 'last_name']
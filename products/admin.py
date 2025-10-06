from django.contrib import admin
from .models import ProductCategory, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'producer_name', 'community', 
        'price_per_kg', 'available_kg', 'status', 'quality', 'created_at'
    ]
    list_filter = [
        'category', 'status', 'quality', 'community', 'region', 'is_organic'
    ]
    search_fields = ['name', 'producer_name', 'community', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Información de Producción', {
            'fields': (
                'producer_name', 'producer_phone', 'community', 'region',
                'harvest_date', 'expiration_date', 'is_organic'
            )
        }),
        ('Información Comercial', {
            'fields': (
                'price_per_kg', 'total_kg', 'available_kg', 
                'status', 'quality'
            )
        }),
        ('Auditoría', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'color', 'is_active', 'product_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    
    def product_count(self, obj):
        return obj.product_set.count()
    product_count.short_description = 'N° Productos'

admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Product, ProductAdmin)
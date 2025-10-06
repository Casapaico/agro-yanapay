from rest_framework import serializers
from .models import Product, ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name', 'description', 'icon', 'color', 'is_active']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'description',
            'price_per_kg', 'total_kg', 'available_kg', 'producer_name',
            'producer_phone', 'community', 'region', 'status', 'quality',
            'image', 'harvest_date', 'expiration_date', 'is_organic',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
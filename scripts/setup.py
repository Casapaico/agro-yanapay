#!/usr/bin/env python
import os
import sys
import django

def setup_project():
    """Configuración rápida del proyecto AgroYanapay"""
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agroyanapay_core.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    from django.contrib.auth import get_user_model
    
    print("🚀 Configurando AgroYanapay...")
    
    # Ejecutar migraciones
    print("📦 Aplicando migraciones...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Crear superusuario si no existe
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        print("👤 Creando superusuario...")
        User.objects.create_superuser(
            username='admin',
            email='admin@agroyanapay.com',
            password='admin123',
            user_type='super_admin'
        )
        print("✅ Superusuario creado: admin / admin123")
    
    # Crear categorías de productos por defecto
    from products.models import ProductCategory
    
    default_categories = [
        {'name': 'Granos', 'icon': '🌾', 'color': '#90AF90'},
        {'name': 'Tubérculos', 'icon': '🥔', 'color': '#59775E'},
        {'name': 'Frutas', 'icon': '🍎', 'color': '#3C4D3C'},
        {'name': 'Verduras', 'icon': '🥦', 'color': '#90AF90'},
        {'name': 'Hierbas', 'icon': '🌿', 'color': '#59775E'},
    ]
    
    for cat_data in default_categories:
        if not ProductCategory.objects.filter(name=cat_data['name']).exists():
            ProductCategory.objects.create(**cat_data)
    
    print("✅ Categorías de productos creadas")
    print("\n🎯 CONFIGURACIÓN COMPLETADA!")
    print("👉 Ejecuta: python manage.py runserver")
    print("🌐 Accede a: http://localhost:8000")
    print("🔐 Admin: http://localhost:8000/admin (admin/admin123)")

if __name__ == '__main__':
    setup_project()
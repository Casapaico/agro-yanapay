from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product-list'),
    path('create/', views.product_create, name='product-create'),
    path('<int:pk>/', views.product_detail, name='product-detail'),
    path('<int:pk>/update/', views.product_update, name='product-update'),
    path('<int:pk>/delete/', views.product_delete, name='product-delete'),
    path('categories/', views.category_list, name='category-list'),
    path('stats/', views.product_stats, name='product-stats'),
]
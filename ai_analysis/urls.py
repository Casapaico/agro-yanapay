from django.urls import path
from . import views

urlpatterns = [
    path('predictions/', views.price_predictions, name='price-predictions'),
    path('analysis/', views.production_analysis, name='production-analysis'),
]
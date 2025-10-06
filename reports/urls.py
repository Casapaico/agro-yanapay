from django.urls import path
from . import views

urlpatterns = [
    path('production/', views.production_reports, name='production-reports'),
    path('whatsapp/', views.whatsapp_reports, name='whatsapp-reports'),
]
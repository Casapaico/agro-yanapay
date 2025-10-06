from django.urls import path
from . import views

urlpatterns = [
    path('reports/', views.whatsapp_reports, name='whatsapp-reports'),
    path('process/<int:report_id>/', views.process_report, name='process-report'),
]
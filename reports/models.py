from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductionReport(models.Model):
    REPORT_TYPE_CHOICES = (
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('monthly', 'Mensual'),
    )
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    total_production_kg = models.DecimalField(max_digits=12, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    community_data = models.JSONField(default=dict)  # Datos por comunidad
    product_data = models.JSONField(default=dict)    # Datos por producto
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='reports/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Reporte de Producción"
        verbose_name_plural = "Reportes de Producción"

class WhatsAppReport(models.Model):
    producer_name = models.CharField(max_length=200)
    producer_phone = models.CharField(max_length=15)
    product_name = models.CharField(max_length=200)
    volume_kg = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    availability_date = models.DateField()
    message_content = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Reporte de WhatsApp"
        verbose_name_plural = "Reportes de WhatsApp"
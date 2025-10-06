from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Ícono")
    color = models.CharField(max_length=7, default='#90AF90', verbose_name="Color")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Categoría de Producto"
        verbose_name_plural = "Categorías de Productos"
    
    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = (
        ('available', 'Disponible'),
        ('sold', 'Vendido'),
        ('reserved', 'Reservado'),
        ('pending', 'Pendiente'),
    )
    
    QUALITY_CHOICES = (
        ('premium', 'Premium'),
        ('standard', 'Estándar'),
        ('basic', 'Básico'),
    )
    
    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, verbose_name="Descripción")
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por Kg (S/.)")
    total_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Kg Disponible")
    available_kg = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Kg Disponibles")
    producer_name = models.CharField(max_length=200, verbose_name="Nombre del Productor")
    producer_phone = models.CharField(max_length=15, blank=True, verbose_name="Teléfono del Productor")
    community = models.CharField(max_length=100, verbose_name="Comunidad")
    region = models.CharField(max_length=100, default='Pasco', verbose_name="Región")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Estado")
    quality = models.CharField(max_length=20, choices=QUALITY_CHOICES, default='standard', verbose_name="Calidad")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Imagen del Producto")
    harvest_date = models.DateField(verbose_name="Fecha de Cosecha")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="Fecha de Vencimiento")
    is_organic = models.BooleanField(default=False, verbose_name="Es Orgánico")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.producer_name} ({self.community})"
    
    def save(self, *args, **kwargs):
        if not self.available_kg:
            self.available_kg = self.total_kg
        super().save(*args, **kwargs)
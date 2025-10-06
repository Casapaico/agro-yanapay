from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView  # ✅ Agregar esto

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ URLs de autenticación de Django
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # ✅ URL del dashboard
    path('dashboard/', TemplateView.as_view(template_name='admin/dashboard.html'), name='dashboard'),
    path('', TemplateView.as_view(template_name='admin/dashboard.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "🌱 AgroYanapay Administration"
admin.site.site_title = "AgroYanapay Admin Portal"
admin.site.index_title = "Bienvenido al Portal de Administración AgroYanapay"
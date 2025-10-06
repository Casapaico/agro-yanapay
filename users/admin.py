from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserSession

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'community', 'is_verified', 'is_active')
    list_filter = ('user_type', 'community', 'is_verified', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Información AgroYanapay', {
            'fields': ('user_type', 'community', 'phone', 'profile_picture', 'is_verified')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información AgroYanapay', {
            'fields': ('user_type', 'community', 'phone', 'profile_picture', 'is_verified')
        }),
    )

class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'ip_address', 'is_active')
    list_filter = ('login_time', 'is_active')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'ip_address', 'user_agent')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserSession, UserSessionAdmin)
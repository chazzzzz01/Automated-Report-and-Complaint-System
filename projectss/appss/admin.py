from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Complaint, Informant, Office

# Customizing the UserAdmin to restrict certain users from admin access
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')

    def has_module_permission(self, request):
        # Only allow access to the admin interface for the superuser created via `createsuperuser`
        if request.user.is_superuser:
            if request.user.username == 'legal_office' or request.user.username.startswith('office_'):
                # Prevent Legal Office and office users from accessing admin
                return False
            return True
        return False  # Deny access to non-superusers

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register Complaint model with admin configuration
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'office', 'type', 'status', 'issue_date', 'is_sent')
    list_filter = ('office', 'status', 'is_sent', 'issue_date')
    search_fields = ('description', 'office', 'type')

admin.site.register(Complaint, ComplaintAdmin)

# Register Informant model with custom display fields
class InformantAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'contact_number', 'department')
    search_fields = ('username', 'email', 'department')
    list_filter = ('role', 'department')

admin.site.register(Informant, InformantAdmin)

# # Register Message model with admin configuration
# class MessageAdmin(admin.ModelAdmin):
#     list_display = ('sender', 'receiver', 'content', 'timestamp')
#     list_filter = ('timestamp',)

# admin.site.register(Message, MessageAdmin)

# Register Office model with admin configuration
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'get_username', 'get_password')
    search_fields = ('office_name', 'user__username')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_password(self, obj):
        return "********"  # Masked password for display
    get_password.short_description = 'Password'

    def save_model(self, request, obj, form, change):
        user = obj.user
        if 'password' in form.changed_data:
            user.set_password(user.password)
        user.save()
        super().save_model(request, obj, form, change)

admin.site.register(Office, OfficeAdmin)

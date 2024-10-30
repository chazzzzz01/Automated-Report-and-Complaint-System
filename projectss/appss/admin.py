


from django.contrib import admin
from .models import Complaint, Informant, Office

# Register Complaint model with admin configuration
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'office', 'type', 'status', 'issue_date', 'is_sent')
    list_filter = ('office', 'status', 'is_sent', 'issue_date')
    search_fields = ('description', 'office', 'type')

admin.site.register(Complaint, ComplaintAdmin)

# Register Informant model with custom display fields
class InformantAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'contact_number', 'department', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'department')
    list_filter = ('role', 'department', 'is_active', 'is_staff', 'is_superuser')
    
     # Override the has_module_permission method to prevent legal office access
    def has_module_permission(self, request):
        # Disallow legal office (superuser) from accessing the Informant admin
        if request.user.is_superuser and request.user.username == 'legal_admin':

            return False
        return super().has_module_permission(request)

    

    # Alternatively, you can also override has_view_permission for more granular control
    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.username == 'legal_admin':
            return False
        return super().has_view_permission(request, obj)

  # Remove username, email, and password fields for the 5 specific accounts
    def get_fields(self, request, obj=None):
        fields = ['username', 'email', 'password']
        if obj and obj.username not in ['GADAdmin', 'vp_admin_finance', 'vp_academic_affairs', 'vp_students_affairs', 'legal_admin']:
            fields.extend(['first_name', 'last_name', 'role', 'contact_number', 'department', 'is_active', 'is_staff', 'is_superuser'])
        return fields

    # Make username, email, and password read-only for the specific office roles
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.username in ['GADAdmin', 'vp_admin_finance', 'vp_academic_affairs', 'vp_students_affairs', 'legal_admin']:
            return ('username', 'email', 'password')
        return []

    # Filter out the office roles from the admin list if they are already created
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

admin.site.register(Informant, InformantAdmin)

# Register Office model with admin configuration
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office_name',)

admin.site.register(Office, OfficeAdmin)


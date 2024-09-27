from django.contrib import admin
from .models import Complaint, Informant, Message

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

# Register Message model
class MessageAdmin(admin.ModelAdmin):
    list_display = ('office', 'content', 'created_at')
    search_fields = ('office', 'content')
    list_filter = ('created_at',)

admin.site.register(Message, MessageAdmin)













from django.contrib import admin
from .models import Office
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

class OfficeAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'get_username', 'get_password')
    search_fields = ('office_name', 'user__username')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_password(self, obj):
        # Return masked password or notify that it is managed through the User model
        return "********"  # Masked password for display
    get_password.short_description = 'Password'

    # Adding inline form to manage user data in the Office admin
    class UserInline(admin.StackedInline):
        model = User
        can_delete = False
        verbose_name_plural = 'User'

    def save_model(self, request, obj, form, change):
        # Save the Office and create User if needed
        user = obj.user
        user.set_password(user.password)
        user.save()
        super().save_model(request, obj, form, change)

admin.site.register(Office, OfficeAdmin)

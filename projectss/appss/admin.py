from django.contrib import admin
from .models import Complaint

class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'office', 'type', 'status', 'issue_date', 'is_sent')
    list_filter = ('office', 'status', 'is_sent', 'issue_date')
    search_fields = ('description', 'office', 'type')

admin.site.register(Complaint, ComplaintAdmin)

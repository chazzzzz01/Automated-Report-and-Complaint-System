from django import forms
from .models import ComplaintReport

class ComplaintReportForm(forms.ModelForm):
    class Meta:
        model = ComplaintReport
        fields = ['description', 'type', 'office']

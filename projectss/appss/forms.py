from django import forms
from .models import Complaint, Message

class ComplaintReportForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description', 'type', 'office']



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
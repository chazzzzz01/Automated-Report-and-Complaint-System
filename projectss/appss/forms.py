from django import forms
from .models import Complaint, Message, Informant

class ComplaintReportForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description', 'type', 'office']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class InformantRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('faculty', 'Faculty'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Informant
        fields = ['role', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'contact_number', 'department']

    def __init__(self, *args, **kwargs):
        super(InformantRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['contact_number'].widget.attrs.update({'placeholder': 'Contact Number'})













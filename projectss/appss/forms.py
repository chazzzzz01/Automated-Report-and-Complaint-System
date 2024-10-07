from django import forms
from .models import Complaint, Informant

class ComplaintReportForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description', 'type', 'office']

# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message
#         fields = ['content']

class InformantRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('faculty', 'Faculty'),
    ]
    
    username = forms.CharField(max_length=150)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Informant
        fields = ['role', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'contact_number', 'department']

    def save(self, commit=True):
        informant = super().save(commit=False)
        informant.set_password(self.cleaned_data['password'])  # Ensure password is hashed
        if commit:
            informant.save()
        return informant
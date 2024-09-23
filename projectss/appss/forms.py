from django import forms
# from django.contrib.auth.models import User  # Import User model for registration
from .models import Complaint, Message
from .models import Informant

# class InformantRegistrationForm(forms.ModelForm):
#     USER_TYPE_CHOICES = [
#         ('student', 'Student'),
#         ('instructor', 'Instructor'),
#         ('staff', 'Staff'),
#     ]
    
#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label='Informant Type')
#     username = forms.CharField(max_length=150, required=True)
#     first_name = forms.CharField(max_length=30, required=True)
#     last_name = forms.CharField(max_length=150, required=True)
#     middle_name = forms.CharField(max_length=150, required=False)

#     class Meta:
#         model = User
#         fields = ['user_type', 'username', 'first_name', 'last_name', 'middle_name']

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
        fields = ['role', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'contact_number']
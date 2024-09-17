from django import forms
# from django.contrib.auth.models import User  # Import User model for registration
from .models import Complaint, Message

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


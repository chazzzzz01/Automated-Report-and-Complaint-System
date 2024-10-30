# from django import forms
# from django.contrib.auth.models import User
# from .models import Complaint, Informant

# class ComplaintReportForm(forms.ModelForm):
#     class Meta:
#         model = Complaint
#         fields = ['description', 'type', 'office']



# from django import forms
# from django.contrib.auth.models import User
# from .models import Informant

# class InformantRegistrationForm(forms.ModelForm):
#     ROLE_CHOICES = [('student', 'Student'), ('employee', 'Employee'), ('faculty', 'Faculty')]

#     username = forms.CharField(max_length=150, required=True)
#     first_name = forms.CharField(max_length=50, required=True)
#     last_name = forms.CharField(max_length=50, required=True)
#     middle_name = forms.CharField(max_length=50, required=False)
#     email = forms.EmailField(required=True)
#     contact_number = forms.CharField(max_length=15, required=True)
#     department = forms.ChoiceField(choices=Informant.DEPARTMENT_CHOICES, required=False)
#     role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)


#     # class Meta:
#     #     model = Informant
#     #     fields = [
#     #         'role', 'username', 'first_name', 'last_name', 'middle_name',
#     #         'email', 'contact_number', 'department'
#     #     ]

#     # # Existing fields...

#     # def save(self, commit=True):
#     #     informant = super().save(commit=False)
#     #     password = self.cleaned_data['password']  # Access cleaned_data from the form

        
#     #     informant.set_password(password)

#     #     if commit:
#     #         informant.save()
#     #         # Sync with User model
#     #         user = User.objects.create_user(username=informant.username, email=informant.email)
#     #         user.set_password(password)  # Hash the password
#     #         user.email = informant.email
#     #         user.first_name = informant.first_name
#     #         user.last_name = informant.last_name
#     #         user.is_active = informant.is_active
#     #         user.is_staff = informant.is_staff
#     #         user.save()

#     #     return informant




#     class Meta:
#         model = Informant
#         fields = ['username', 'email', 'first_name', 'last_name', 'contact_number', 'role', 'department']

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         informant = super().save(commit=False)
#         informant.set_password(self.cleaned_data["password1"])
#         if commit:
#             informan-t.save()
#         return informant

# class InformantLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)








from django import forms
from .models import Complaint, Informant
from django import forms
from appss.models import Informant
from django.contrib.auth.forms import UserCreationForm

class ComplaintReportForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['description', 'type', 'office']

class InformantRegistrationForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('faculty', 'Faculty'),
    ]
    
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    middle_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField(required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    department = forms.ChoiceField(choices=Informant.DEPARTMENT_CHOICES, required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Informant
        fields = ['role', 'username', 'first_name', 'last_name', 'middle_name', 'email', 'contact_number', 'department',  'student_id_file', 'study_load_file', 'employee_id_file', 'document_file']

    def save(self, commit=True):
        informant = super().save(commit=False)
        informant.set_password(self.cleaned_data['password'])  # Ensure password is hashed
        if commit:
            informant.save()
        return informant

# class InformantRegistrationForm(UserCreationForm):
#     class Meta:
#         model = Informant
#         fields = ['email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser']

#     def save(self, commit=True):
#         informant = super().save(commit=False)
#         informant.set_password(self.cleaned_data['password1'])  # Use password1 for the hashed password
#         if commit:
#             informant.save()
#         return informant




from django import forms
from .models import Complaint

class ResponseForm(forms.Form):
    letter_content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full p-2 border border-gray-300 rounded',
        'placeholder': 'Type your response here...',
        'rows': 5
    }), label='Letter Content')
    complaint_id = forms.IntegerField(widget=forms.HiddenInput())

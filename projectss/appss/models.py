from django.db import models
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.contrib.auth.models import User
import re





from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User,  Group, Permission
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Custom User Manager for Informant
class InformantManager(BaseUserManager):
    def create_user(self, username, email, password=None, is_staff=False, is_superuser=False):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user
    
    # def create_user(self, username, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)

    #     return self.create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password):
        return self.create_user(username, email=email, password=password, is_staff=True, is_superuser=True)

# Informant model with extended fields
class Informant(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('faculty', 'Faculty'),
    ]

    DEPARTMENT_CHOICES = [
        ('STCS', 'School of Technology and Computer Science'),
        ('SCJE', 'School of Criminal Justice and Education'),
        ('SAS', 'School of Arts and Sciences'),
        ('SME', 'School of Management and Entrepreneurship'),
        ('SOE', 'School of Engineering'),
        ('SNHS', 'School of Nursing and Health Sciences'),
        ('STED', 'School of Teacher Education'),
    ]

    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    student_id_file = models.ImageField(null=True, blank=True)
    employee_id_file = models.ImageField(null=True, blank=True)
    study_load_file = models.ImageField(null=True, blank=True)
    document_file = models.ImageField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='informant_set',  # Add a custom related name to avoid conflicts with auth.User
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='informant_set',  # Add a custom related name to avoid conflicts with auth.User
        blank=True
    )


    objects = InformantManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

      # Add related_name to groups and user_permissions to avoid conflicts with auth.User
    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='informant_set',  # Avoid conflict with auth.User
    #     blank=True,
    #     help_text='The groups this user belongs to.',
    #     verbose_name='groups'
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='informant_user_permissions',  # Avoid conflict with auth.User
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions'
    # )

    # USERNAME_FIELD = 'username'  # or username if you prefer
    # REQUIRED_FIELDS = ['first_name', 'last_name', 'contact_number', 'department']

    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']

    # def save(self, *args, **kwargs):
    #     # Save the Informant first
    #     super(Informant, self).save(*args, **kwargs)

    #     # Create or update the corresponding User model instance
    #     if not self.user:  # Only create a new User if one doesn't exist
    #         user = User.objects.create_user(username=self.username, email=self.email)
    #         user.email = self.email
    #         user.first_name = self.first_name
    #         user.last_name = self.last_name
    #         user.is_active = self.is_active
    #         user.is_staff = self.is_staff
    #         # user.set_password(self.password)  # Hash the password only for new users
    #         user.set_password(self.password)  # Hash the password correctly
    #         user.save()
    #         self.user = user
           
            
    #     else:
    #         # Update existing User information
    #         self.user.username = self.username
    #         self.user.email = self.email
    #         self.user.first_name = self.first_name
    #         self.user.last_name = self.last_name
    #         self.user.is_active = self.is_active
    #         self.user.is_staff = self.is_staff
    #         if self.password:  # If the password field is set
    #           self.user.set_password(self.password)  # Use set_password to hash the password
    #         self.user.save()
  
    #         self.user.save()


    #         super(Informant, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"



# Office Model
class Office(models.Model):
    OFFICE_CHOICES = [
        ('GAD Office', 'GAD Office'),
        ('VP Administration and Finance', 'Admin and Finance'),
        ('VP Academic Affairs', 'VP Academic Affairs'),
        ('VP Students and External Affairs', 'VP Students and External Affairs'),
    ]

    office_name = models.CharField(max_length=50, choices=OFFICE_CHOICES, unique=True)
    informant = models.OneToOneField(Informant, on_delete=models.CASCADE)   # Linking office to the default user model

    def __str__(self):
        return self.office_name


# Complaint Model with PDF generation
class Complaint(models.Model):
    TYPE_CHOICES = [
        ('report', 'Report'),
        ('complaint', 'Complaint')
    ]
    STATUS_CHOICES = [
        ('Solved', 'Solved'),
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress')
    ]
    OFFICE_CHOICES = [
        ('VP Administration and Finance', 'Admin and Finance'),
        ('VP Academic Affairs', 'VP Academic Affairs'),
        ('VP Students and External Affairs', 'VP Students and External Affairs'),
        ('GAD Office', 'GAD Office'),
    ]
    
    CATEGORY_CHOICES = [
    ('sexual_harassment', 'Sexual Harassment'),
    ('sexual_assault', 'Sexual Assault'),
    ('bullying', 'Bullying'),
    ('discrimination', 'Discrimination'),
    ('abuse', 'Abuse'),
    ('violence', 'Violence'),
    ('gender_equality', 'Gender Equality'),
     ('defamation', 'Defamation'),
    ('rape', 'Rape'),

    # Financial Issues
    ('financial_issues', 'Financial Issues'),
    ('scholarship_issues', 'Scholarship Issues'),
    ('late_fees', 'Late Fees'),
    ('financial_aid', 'Financial Aid'),
    ('staff_payment_issues', 'Staff Payment Issues'),
    ('billing_errors', 'Billing Errors'),

    # Staff and Academic Concerns
    ('staff_academic_concerns', 'Staff and Academic Concerns'),
    ('tardiness', 'Tardiness'),
    ('always_late', 'Always Late'),
    ('favoritism', 'Favoritism'),
    ('always_absent', 'Always Absent'),
    ('unfair_grading', 'Unfair Grading'),
    ('unprofessional_behavior', 'Unprofessional Behavior'),

    # Student-Related Issues
    ('student_related_issues', 'Student-Related Issues'),
    ('student_misconduct', 'Student Misconduct'),
    ('student_welfare', 'Student Welfare'),
    ('student_engagement', 'Student Engagement'),
    ('student_rights', 'Student Rights'),
   
   


   
   

]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    office = models.CharField(max_length=50, choices=OFFICE_CHOICES)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES) 
    status = models.CharField(max_length=50, default='Pending', choices=STATUS_CHOICES)
    urgency = models.CharField(max_length=50)
    pdf_file = models.FileField(upload_to='complaint_pdfs/', null=True, blank=True)
    informant = models.ForeignKey(Informant, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    receiving_office = models.CharField(max_length=50, choices=OFFICE_CHOICES)
    informant = models.ForeignKey(Informant, null=True, on_delete=models.CASCADE)  # Link to the Informant
    
    


    def save(self, *args, **kwargs):
        if not self.pdf_file:
            self.pdf_file = self.generate_pdf()
        super().save(*args, **kwargs)

    def generate_pdf(self):
        
        buffer = BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(name='TitleStyle', fontSize=14, alignment=1)
        header_style = ParagraphStyle(name='HeaderStyle', fontSize=12, alignment=0)
        body_style = ParagraphStyle(name='BodyStyle', fontSize=12, alignment=0, spaceAfter=12)

        story = []

        # PDF content
        story.append(Paragraph(f"Date: {timezone.now().strftime('%B %d, %Y')}", header_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"To: {self.office}", header_style))
        story.append(Spacer(1, 12))
        

        # complaint details
        story.append(Paragraph(f"Label: {self.category}", body_style))
        story.append(Paragraph(f"Urgency: {self.urgency}", body_style))
        story.append(Paragraph(f"Type: {self.type}", body_style))

        story.append(Spacer(1, 12))   
        story.append(Paragraph("Description:", body_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph(self.description, body_style))

        # closing
        story.append(Spacer(1, 24))
        story.append(Paragraph("Sincerely,", body_style))
        
          # Adding informant's username
        story.append(Spacer(1, 12))
        story.append(Paragraph(self.informant.username, body_style))

        pdf.build(story)

        buffer.seek(0)
        filename = f"complaint_{self.id}_description.pdf"
        return ContentFile(buffer.getvalue(), filename)

    def count_keyword_occurrences(self, keyword):
        """
        Counts occurrences of a specific keyword in the description.
        """
        # Use case-insensitive search
        pattern = re.compile(rf'\b{keyword}\b', re.IGNORECASE)
        return len(pattern.findall(self.description))
    
    def contains_sensitive_keywords(self):
        """
        Checks if description contains sensitive keywords like 'sexual harassment'.
        """
        keywords = ['sexual harassment', 'harassment']  # Add more keywords as needed
        for keyword in keywords:
            if self.count_keyword_occurrences(keyword) > 0:
                return True
        return False

# Additional Models
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Urgency(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    


class Response(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    letter_content = models.TextField()
    response_pdf = models.FileField(upload_to='responses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    



from django.db import models

# Define the possible offices and departments
OFFICE_CHOICES = [
    ('GAD', 'Gender and Development'),
    ('AA', 'Academic Affairs'),
    ('AF', 'Admin and Finance'),
    ('SA', 'Student Affairs'),
]

DEPARTMENT_CHOICES = [
    ('STCS', 'School of Technology and Computer Science'),
    ('SCJE', 'School of Criminal Justice and Education'),
    ('SAS', 'School of Arts and Sciences'),
    ('SME', 'School of Management and Entrepreneurship'),
    ('SOE', 'School of Engineering'),
    ('SNHS', 'School of Nursing and Health Sciences'),
    ('STED', 'School of Teacher Education'),
]

CATEGORY_CHOICES = [
    ('sexual_harassment', 'Sexual Harassment'),
    ('sexual_assault', 'Sexual Assault'),
    ('bullying', 'Bullying'),
    ('discrimination', 'Discrimination'),
    ('abuse', 'Abuse'),
    ('violence', 'Violence'),
    ('gender_equality', 'Gender Equality'),
     ('defamation', 'Defamation'),
    ('rape', 'Rape'),

    # Financial Issues
    ('financial_issues', 'Financial Issues'),
    ('scholarship_issues', 'Scholarship Issues'),
    ('late_fees', 'Late Fees'),
    ('financial_aid', 'Financial Aid'),
    ('staff_payment_issues', 'Staff Payment Issues'),
    ('billing_errors', 'Billing Errors'),

    # Staff and Academic Concerns
    ('staff_academic_concerns', 'Staff and Academic Concerns'),
    ('tardiness', 'Tardiness'),
    ('always_late', 'Always Late'),
    ('favoritism', 'Favoritism'),
    ('always_absent', 'Always Absent'),
    ('unfair_grading', 'Unfair Grading'),
    ('unprofessional_behavior', 'Unprofessional Behavior'),

    # Student-Related Issues
    ('student_related_issues', 'Student-Related Issues'),
    ('student_misconduct', 'Student Misconduct'),
    ('student_welfare', 'Student Welfare'),
    ('student_engagement', 'Student Engagement'),
    ('student_rights', 'Student Rights'),
   
   

]

# Define the Incident model
class Incident(models.Model):
    office = models.CharField(max_length=3, choices=OFFICE_CHOICES)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES)
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    incident_content = models.TextField()

    def __str__(self):
        return f'{self.department} - {self.office}'


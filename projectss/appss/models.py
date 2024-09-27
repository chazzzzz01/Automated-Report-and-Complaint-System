from django.db import models
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.contrib.auth.models import User


class Informant(models.Model):
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
        ('LHS', 'Liberal Arts and Humanities'),
        ('STED', 'School of Teacher Education'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    department = models.CharField(max_length=4, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    student_id_file = models.ImageField(upload_to='student_ids/', null=True, blank=True)
    employee_id_file = models.ImageField(upload_to='employee_ids/', null=True, blank=True)
    study_load_file = models.ImageField(upload_to='study_loads/', null=True, blank=True)
    document_file = models.ImageField(upload_to='documents/', null=True, blank=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)

    def __str__(self):
        
        return f"{self.username} ({self.role})"

class Office(models.Model):
    OFFICE_CHOICES = [
        ('GAD Office', 'GAD Office'),
        ('VP Administration and Finance', 'Admin and Finance'),
        ('VP Academic Affairs', 'VP Academic Affairs'),
        ('VP Students and External Affairs', 'VP Students and External Affairs'),
    ]
    
    office_name = models.CharField(max_length=50, choices=OFFICE_CHOICES, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking office to a user account

    def __str__(self):
        return self.office_name

# Complaint Model
class Complaint(models.Model):
    OFFICE_CHOICES = [
        ('VP Administration and Finance', 'Admin and Finance'),
        ('VP Academic Affairs', 'VP Academic Affairs'),
        ('VP Students and External Affairs', 'VP Students and External Affairs'),
        ('GAD Office', 'GAD Office'),
    ]

    description = models.TextField()
    office = models.CharField(max_length=50, choices=OFFICE_CHOICES)
    type = models.CharField(max_length=50) 
    status = models.CharField(max_length=50, default='Pending')
    urgency = models.CharField(max_length=50) 
    pdf_file = models.FileField(upload_to='complaint_pdfs/', null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    

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

        # header
        story.append(Paragraph(f"Date: {timezone.now().strftime('%B %d, %Y')}", header_style))
        story.append(Spacer(1, 1))
        story.append(Paragraph(f"To: {self.office}", header_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Subject: {self.type}", header_style))
        story.append(Spacer(1, 24))

        # letter body
        story.append(Paragraph(f"Dear Sir/Madam,", body_style))
        story.append(Spacer(1, 12))

        # complaint details
        story.append(Paragraph(f"Issue Date: {self.issue_date.strftime('%B %d, %Y')}", body_style))
        story.append(Paragraph(f"Urgency: {self.urgency}", body_style))  # Still in process
        story.append(Paragraph(f"Type: {self.type}", body_style))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("Description:", body_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph(self.description, body_style))

        # closing
        story.append(Spacer(1, 24))
        story.append(Paragraph("Sincerely,", body_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Your Name", body_style))  # still didnt have the registration and login form, still no username

        pdf.build(story)

        buffer.seek(0)
        filename = f"complaint_{self.id}_description.pdf"
        return ContentFile(buffer.getvalue(), filename)


class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Urgency(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Still in Process

    def __str__(self):
        return self.name



# Still in process
class Message(models.Model):
    office = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.office}: {self.content}'
    



from django.db import models
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# New Urgency model
class Urgency(models.Model):
    LEVEL_CHOICES = [
        ('High', 'High'),
        ('Low', 'Low'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.level

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
        
        # Custom styles for letter format
        title_style = ParagraphStyle(name='TitleStyle', fontSize=14, alignment=1)
        header_style = ParagraphStyle(name='HeaderStyle', fontSize=12, alignment=0)
        body_style = ParagraphStyle(name='BodyStyle', fontSize=12, alignment=0, spaceAfter=12)

        story = []

        # Add header information
        story.append(Paragraph(f"Date: {timezone.now().strftime('%B %d, %Y')}", header_style))
        story.append(Spacer(1, 1))
        story.append(Paragraph(f"To: {self.office}", header_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Subject: {self.type}", header_style))
        story.append(Spacer(1, 24))

        # Add letter body
        story.append(Paragraph(f"Dear Sir/Madam,", body_style))
        story.append(Spacer(1, 12))
        
        # Add complaint details
        story.append(Paragraph(f"Issue Date: {self.issue_date.strftime('%B %d, %Y')}", body_style))
        story.append(Paragraph(f"Date and Time of Description: {timezone.now().strftime('%B %d, %Y %H:%M:%S')}", body_style))
        story.append(Paragraph(f"Type: {self.type}", body_style))
        story.append(Paragraph(f"Urgency Level: {self.urgency.level}", body_style))  # Updated to use urgency level from related model
        story.append(Spacer(1, 12))
        story.append(Paragraph("Description:", body_style))
        story.append(Spacer(1, 6))
        story.append(Paragraph(self.description, body_style))

        # Add closing
        story.append(Spacer(1, 24))
        story.append(Paragraph("Sincerely,", body_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Your Name", body_style))  # You might want to replace this with the actual user's name

        pdf.build(story)

        buffer.seek(0)
        filename = f"complaint_{self.id}_description.pdf"
        return ContentFile(buffer.getvalue(), filename)










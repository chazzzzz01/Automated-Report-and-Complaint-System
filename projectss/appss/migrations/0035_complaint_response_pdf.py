# Generated by Django 5.1.1 on 2024-10-19 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0034_remove_complaint_response_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='response_pdf',
            field=models.FileField(blank=True, null=True, upload_to='response_pdfs/'),
        ),
    ]
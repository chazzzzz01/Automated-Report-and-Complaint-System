# Generated by Django 5.1.1 on 2024-10-19 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0037_remove_complaint_response_pdf_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='response_pdf',
            field=models.FileField(blank=True, null=True, upload_to='responses/'),
        ),
        migrations.DeleteModel(
            name='Response',
        ),
    ]

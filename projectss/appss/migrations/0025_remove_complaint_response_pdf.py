# Generated by Django 5.1.1 on 2024-10-18 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0024_remove_officeresponse_complaint_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='response_pdf',
        ),
    ]
# Generated by Django 5.0.7 on 2024-08-18 06:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appss", "0002_complaint_pdf_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complaint",
            name="pdf_file",
            field=models.FileField(blank=True, null=True, upload_to="complaints/"),
        ),
    ]

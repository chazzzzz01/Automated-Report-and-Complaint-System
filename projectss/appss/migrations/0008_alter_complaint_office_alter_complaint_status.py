# Generated by Django 5.0.7 on 2024-08-18 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appss", "0007_alter_complaint_office_alter_complaint_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="complaint",
            name="office",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="complaint",
            name="status",
            field=models.CharField(default="Pending", max_length=50),
        ),
    ]
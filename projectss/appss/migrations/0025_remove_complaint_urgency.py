# Generated by Django 5.0.7 on 2024-09-04 09:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("appss", "0024_alter_complaint_urgency"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="complaint",
            name="urgency",
        ),
    ]

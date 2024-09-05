# Generated by Django 5.0.7 on 2024-09-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appss", "0039_alter_complaint_urgency"),
    ]

    operations = [
        migrations.CreateModel(
            name="Urgency",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "level",
                    models.CharField(
                        choices=[("High", "High"), ("Low", "Low")],
                        max_length=10,
                        unique=True,
                    ),
                ),
            ],
        ),
    ]

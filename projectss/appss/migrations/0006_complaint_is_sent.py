# Generated by Django 5.0.7 on 2024-08-18 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appss", "0005_complaint_issue_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="complaint",
            name="is_sent",
            field=models.BooleanField(default=False),
        ),
    ]

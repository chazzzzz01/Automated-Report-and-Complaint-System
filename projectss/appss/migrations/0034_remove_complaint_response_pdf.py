# Generated by Django 5.1.1 on 2024-10-19 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0033_delete_letter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='response_pdf',
        ),
    ]

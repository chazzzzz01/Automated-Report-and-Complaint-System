# Generated by Django 5.1.1 on 2024-10-13 02:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0019_remove_complaint_informant'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='informant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

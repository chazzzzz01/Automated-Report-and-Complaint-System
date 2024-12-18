# Generated by Django 5.1.1 on 2024-10-17 05:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0022_alter_informant_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('office', models.CharField(max_length=50)),
                ('message', models.TextField()),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='office_responses_pdfs/')),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('complaint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='office_responses', to='appss.complaint')),
            ],
        ),
    ]

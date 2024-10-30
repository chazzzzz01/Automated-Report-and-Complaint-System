# Generated by Django 5.1.1 on 2024-10-18 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0025_remove_complaint_response_pdf'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OfficeResponse',
        ),
        migrations.RemoveField(
            model_name='complaint',
            name='informant',
        ),
        migrations.AlterField(
            model_name='complaint',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='type',
            field=models.CharField(max_length=50),
        ),
    ]

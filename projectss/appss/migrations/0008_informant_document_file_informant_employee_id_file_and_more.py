# Generated by Django 5.1.1 on 2024-10-08 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0007_remove_informant_document_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='informant',
            name='document_file',
            field=models.ImageField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AddField(
            model_name='informant',
            name='employee_id_file',
            field=models.ImageField(blank=True, null=True, upload_to='employee_ids/'),
        ),
        migrations.AddField(
            model_name='informant',
            name='student_id_file',
            field=models.ImageField(blank=True, null=True, upload_to='student_ids/'),
        ),
        migrations.AddField(
            model_name='informant',
            name='study_load_file',
            field=models.ImageField(blank=True, null=True, upload_to='study_loads/'),
        ),
        migrations.AlterField(
            model_name='informant',
            name='department',
            field=models.CharField(blank=True, choices=[('STCS', 'School of Technology and Computer Science'), ('SCJE', 'School of Criminal Justice and Education'), ('SAS', 'School of Arts and Sciences'), ('SME', 'School of Management and Entrepreneurship'), ('SOE', 'School of Engineering'), ('SNHS', 'School of Nursing and Health Sciences'), ('LHS', 'Liberal Arts and Humanities'), ('STED', 'School of Teacher Education')], max_length=4, null=True),
        ),
    ]

# Generated by Django 5.1.1 on 2024-10-10 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appss', '0013_alter_informant_user_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informant',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
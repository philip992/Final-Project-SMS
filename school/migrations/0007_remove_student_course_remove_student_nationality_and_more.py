# Generated by Django 5.1.1 on 2025-06-01 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0006_student_address_student_nationality_student_phone_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='course',
        ),
        migrations.RemoveField(
            model_name='student',
            name='nationality',
        ),
        migrations.RemoveField(
            model_name='student',
            name='status',
        ),
        migrations.RemoveField(
            model_name='student',
            name='year_level',
        ),
    ]

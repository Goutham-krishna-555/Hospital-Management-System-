# Generated by Django 5.1.3 on 2024-12-05 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_appointment_date_alter_appointment_doctor_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='admission_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='payment',
            name='discharge_date',
            field=models.DateField(),
        ),
    ]

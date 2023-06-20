# Generated by Django 4.2.2 on 2023-06-19 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiologyDepartment', '0003_patient_phone_number_alter_appointment_due_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='cost',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='status',
            field=models.CharField(choices=[('R', 'Ready'), ('N', 'Not Ready'), ('C', 'Completed')], default='N', max_length=1),
        ),
    ]
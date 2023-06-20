# Generated by Django 4.2.2 on 2023-06-18 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiologyDepartment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardiologist',
            name='experience',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='cardiologist',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='cardiologist',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cardiologist',
            name='phone_number',
            field=models.CharField(max_length=14, null=True),
        ),
        migrations.AlterField(
            model_name='cardiologist',
            name='specialization',
            field=models.CharField(choices=[('g', 'General cardiology'), ('c', 'Cardiac electrophysiology'), ('e', 'Echocardiography'), ('h', 'Heart failure and transplant cardiology')], default='g', max_length=1, null=True),
        ),
    ]
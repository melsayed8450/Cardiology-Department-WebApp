from typing import Any
from django.db import models


class Cardiologist(models.Model):
    GENDER_CHOICES = (('m','male'),('f','female'))
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    SPECIALIZATIONS = (
        ('G','General cardiology'),
        ('C','Cardiac electrophysiology'),
        ('E','Echocardiography'),
        ('H','Heart failure and transplant cardiology'),
    )
    name = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=3, null=True,blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=GENDER_MALE)
    brief_info = models.TextField(null=True,blank=True)
    specialization = models.CharField(max_length=1, choices=SPECIALIZATIONS,default='G',null=True)
    phone_number = models.CharField(max_length=14,null=True)
    experience = models.CharField(max_length=2,null=True)
    def __str__(self):
        return self.name



class Patient(models.Model):
    GENDER_CHOICES = (('m','male'),('f','female'))
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    cardiologist = models.ForeignKey(Cardiologist,on_delete=models.SET_NULL,null=True)
    nurse = models.ForeignKey('Nurse',on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=3, null=True,blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default=GENDER_MALE)
    insurance_details = models.TextField(null=True,blank=True)
    medical_history = models.TextField(null=True,blank=True)
    phone_number = models.CharField(max_length=14,null=True)
    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL,null=True)
    cardiologist = models.ForeignKey(Cardiologist,on_delete=models.SET_NULL,null=True)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)
     
    


class Test(models.Model):
    STATUS_CHOICES = (
        ('R','Ready'),
        ('N','Not Ready'),
        ('C','Completed'),
    )
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL,null=True)
    cardiologist = models.ForeignKey(Cardiologist,on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=100,null=True)
    cost = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='N')
    def __str__(self):
        return self.name


class Nurse(models.Model):
    name = models.CharField(max_length=100,null=True)
    age = models.CharField(max_length=3, null=True,blank=True)
    phone_number = models.CharField(max_length=14,null=True)
    def __str__(self):
        return self.name
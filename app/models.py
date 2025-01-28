from django.db import models
from django.db.models import IntegerField


# Create your models here.
class Patient(models.Model):
    patient_name=models.CharField(max_length=100)
    date_of_birth=models.CharField(max_length=100)
    age=models.IntegerField()
    phone=models.IntegerField()
    medical_history=models.CharField(max_length=100, blank=True)
    status=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    gender=models.CharField(max_length=50)
    address=models.TextField()

    def __str__(self):
        return self.patient_name

class Doctor(models.Model):
    doctor_name=models.CharField(max_length=100)
    date_of_birth=models.CharField(max_length=100)
    specialization=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    age=models.IntegerField()
    phone=models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    availability=models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.doctor_name

class Appointment(models.Model):
    patient_id = models.IntegerField()
    patient_name = models.CharField(max_length=100)
    department=models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    date1= models.DateField()
    email=models.EmailField()
    time_slot=models.CharField(max_length=100)
    status=models.CharField(max_length=50)
    problem = models.CharField(max_length=150)

    def __str__(self):
        return self.patient_name

class Payment(models.Model):
    patient_id=models.IntegerField()
    patient_name=models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=100)
    admission_date=models.DateField()
    discharge_date = models.DateField()
    room_charge = models.IntegerField()
    doctor_fee=models.IntegerField()
    medicine_cost = models.IntegerField()
    other_charge = models.IntegerField()

    def __str__(self):
        return self.patient_name

    def total(self):
        return self.room_charge + self.doctor_fee + self.medicine_cost + self.other_charge



"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',views.BASE,name='base'),
    #patient
    path('Patient/add/',views.ADD_PATIENT,name='add_patient'),
    path('Patient/view_patients',views.VIEW_PATIENTS,name='view_patients'),
    path('Patient/delete_patient/<int:patient_id>/', views.delete_patient, name='delete_patient'),
    path('Patients/edit_patients/<str:id>/', views.edit_patients, name='edit_patient'),
    path('Patients/update_patient/',views.update_patient,name='update_patient'),
    #login path
    path('login/',views.LOGIN,name='login'),

    #home
    path('',views.HOME,name='home'),

    #doctor
    path('Doctors/add/',views.add_doctor,name='add_doctor'),
    path('Doctors/view/',views.view_doctors, name='view_doctors'),
    path('Doctors/edit/<str:id>/',views.edit_doctors,name='edit_doctors'),
    path('Doctor/delete/<int:doctor_id>/',views.delete_doctor,name='delete_doctor'),
    path('Doctor/update/',views.update_doctor,name='update_doctor'),

    #appointment
    path('Appointment/add/',views.add_appointment,name='add_appointment'),
    path('Appointment/view/',views.view_appointments, name='view_appointments'),
    path('Appointment/edit/<str:id>/',views.edit_appointment,name='edit_appointment'),
    path('Appointment/delete/<int:appointment_id>/',views.delete_appointment,name='delete_appointment'),
    path('Appointment/update/',views.update_appointment,name='update_appointment'),

    #payments
    path('Payments/add/',views.add_payment,name='add_payment'),
    path('Payments/view/',views.view_payment,name='view_payment'),
    path('Payments/delete/<int:payment_id>',views.delete_payment,name='delete_payment'),
    path('Payments/edit/<str:id>/',views.edit_payment,name='edit_payment'),
    path('Payments/update/',views.update_payment,name='update_payment'),
    path('Payments/generate_bill/<int:payment_id>/',views.generate_payment_bill,name='generate_payment_bill'),

    #reminder
    path('send-reminder/<int:appointment_id>/', views.send_reminder, name='send_reminder'),

    #appointment page csv and pdf
    path('export_appointments_csv/', views.export_appointments_csv, name='export_appointments_csv'),
    path('export_appointments_pdf/', views.export_appointments_pdf, name='export_appointments_pdf'),

    #doctors page csv and pdf
    path('export_doctors_csv/', views.export_doctors_csv, name='export_doctors_csv'),
    path('export_doctors_pdf/', views.export_doctors_pdf, name='export_doctors_pdf'),

    path('export_patients_csv/', views.export_patients_csv, name='export_patients_csv'),
    path('export_patients_pdf/', views.export_patients_pdf, name='export_patients_pdf'),


]

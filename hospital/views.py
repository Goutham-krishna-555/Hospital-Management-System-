from django.shortcuts import render ,redirect
from django.template.loader_tags import do_block
from app.models import Patient
from app.models import Doctor
from app.models import Appointment
from app.models import Payment
from datetime import datetime
from datetime import timedelta
from django.core.mail import send_mail
import calendar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.template.loader import render_to_string
from django.template.loader import get_template
import os
from xhtml2pdf import pisa
from django.utils.timezone import now
from django.db.models import Q
import csv
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from pyexpat.errors import messages
from app.utils import export_to_csv, export_to_pdf
from torch.distributed.autograd import context



def BASE(request):
    return render(request, 'base.html')


def ADD_PATIENT(request):
    if request.method=='POST':
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        medical_history=request.POST.get('medical_history')
        status=request.POST.get('status')
        gender = request.POST.get('gender')
        address = request.POST.get('address')

        patient = Patient(
            patient_name=patient_name,
            date_of_birth=dob,
            age = age,
            phone=phone,
            gender=gender,
            email=email,
            medical_history=medical_history,
            status=status,
            address=address,
        )
        patient.save()
    return render(request,'patients/add_patient.html')


def LOGIN(request):
    return render(request,'login.html')

from django.utils.timezone import localtime
def HOME(request):
    # Fetch data for KPIs
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    completed_appointments = Appointment.objects.filter(status="Completed").count()
    pending_appointments = Appointment.objects.filter(status="Pending").count()

    doctors = Doctor.objects.values('doctor_name', 'specialization', 'availability')

    server_time = now()

    # Manually adjust the time by adding 5 hours (the time difference you mentioned)
    adjusted_time = server_time + timedelta(hours=5)

    # Get today's date based on the adjusted time
    today = adjusted_time.date()  # Get today's date based on the server's local time zone

    # Filter appointments where the date part of date1 is greater than or equal to today
    upcoming_appointments = Appointment.objects.filter(date1__gte=today).order_by('date1').values(
        'id', 'patient_name', 'doctor_name', 'date1', 'time_slot', 'status'
    )

    # Generate a pie chart for appointment status
    labels = ['Completed', 'Pending']
    sizes = [completed_appointments, pending_appointments]
    colors = ['#4CAF50', '#FFC107']
    explode = (0.1, 0)  # explode first slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    pie_chart = BytesIO()
    plt.savefig(pie_chart, format='png')
    pie_chart.seek(0)
    pie_chart_url = base64.b64encode(pie_chart.getvalue()).decode('utf8')
    plt.close(fig)



    # Prepare data for bar chart (Appointments per Month)
    current_year = datetime.now().year
    months = range(1, 13)  # January (1) to December (12)
    monthly_counts = [
        Appointment.objects.filter(date1__month=month, date1__year=current_year).count() for month in months
    ]
    month_names = [calendar.month_name[month] for month in months]

    # Create a smaller bar chart
    fig, ax = plt.subplots(figsize=(9, 7))  # Smaller figure size
    ax.bar(month_names, monthly_counts, color='#2196F3')
    ax.set_xlabel('Month')
    ax.set_ylabel('Appointments')
    ax.set_title(f'Appointments by Month in {current_year}')
    ax.tick_params(axis='x', rotation=45)

    bar_chart = BytesIO()
    plt.savefig(bar_chart, format='png')
    bar_chart.seek(0)
    bar_chart_url = base64.b64encode(bar_chart.getvalue()).decode('utf8')
    plt.close(fig)



    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'total_appointments': total_appointments,
        'pie_chart_url': pie_chart_url,
        'bar_chart_url': bar_chart_url,
        'doctors': doctors,
        'upcoming_appointments': upcoming_appointments,

    }

    return render(request, 'home.html', context)


def bubble_sort(patients, reverse=False):
    n = len(patients)
    # Traverse through all elements in the list
    for i in range(n):
        # Last i elements are already sorted, so no need to check them again
        for j in range(0, n-i-1):
            # If sorting in ascending order or descending order, swap if needed
            if (patients[j].patient_name > patients[j+1].patient_name) != reverse:
                # Swap if the element found is greater (or smaller for descending) than the next element
                patients[j], patients[j+1] = patients[j+1], patients[j]
    return patients



def selection_sort(patients, reverse=False):
    for i in range(len(patients)):
        target_index = i
        for j in range(i + 1, len(patients)):
            if (patients[j].patient_name < patients[target_index].patient_name) != reverse:
                target_index = j
        patients[i], patients[target_index] = patients[target_index], patients[i]
    return patients



def insertion_sort(patients, reverse=False):
    for i in range(1, len(patients)):
        key = patients[i]
        j = i - 1
        while j >= 0 and (key.patient_name < patients[j].patient_name) != reverse:
            patients[j + 1] = patients[j]
            j -= 1
        patients[j + 1] = key
    return patients

# Linear Search
def linear_search(query, patients):
    # Convert query to lowercase to make it case-insensitive
    query = query.lower()
    result = [patient for patient in patients if query in patient.patient_name.lower()]
    return result


def binary_search(query, patients):
    # Convert query to lowercase to make it case-insensitive
    query = query.lower()
    left, right = 0, len(patients) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_name = patients[mid].patient_name.lower()

        if mid_name == query:
            return patients[mid]  # Exact match found
        elif mid_name < query:
            left = mid + 1
        else:
            right = mid - 1

    return None  # Not found


def VIEW_PATIENTS(request):
    query = request.GET.get('search','')
    sort_method = request.GET.get('sort_method', 'default_sort')
    sort_order = request.GET.get('sort_order', 'asc')
    search_method = request.GET.get('search_method', 'linear_search')  # Default search method

    reverse = True if sort_order == 'desc' else False

    if query:
        patients = Patient.objects.all()

        # Choose the search method based on user input
        if search_method == 'linear_search':
            patients = linear_search(query, patients)
    else:
        patients = Patient.objects.all()
        if sort_method == 'bubble_sort':
            patients = list(patients)  # Convert QuerySet to list to apply quicksort
            patients = bubble_sort(patients, reverse)
        elif sort_method == 'selection_sort':
            patients = list(patients)  # Convert QuerySet to list to apply selection sort
            patients = selection_sort(patients, reverse)
        elif sort_method == 'insertion_sort':
            patients = list(patients)  # Convert QuerySet to list to apply insertion sort
            patients = insertion_sort(patients, reverse)
        elif sort_method == 'default_sort':
            patients = patients.order_by('patient_name' if not reverse else '-patient_name')

    context = {'patients': patients}
    return render(request, 'patients/view_patients.html', context)


from django.shortcuts import redirect

def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, pk=patient_id)
        patient.delete()
        return redirect('view_patients')
    else:
        return HttpResponseForbidden()




def edit_patients(request,id):
    patient=Patient.objects.filter(id = id)

    context={
        'patient':patient,
    }
    return render(request, 'patients/edit_patients.html',context)


def update_patient(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')
        dob = request.POST.get('dob')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        medical_history=request.POST.get('medical_history')
        status=request.POST.get('status')
        address = request.POST.get('address')

        patient=Patient.objects.get(id=patient_id)
        patient.patient_name=patient_name
        patient.date_of_birth = dob
        patient.age = age
        patient.phone = phone
        patient.email = email
        patient.gender = gender
        patient.medical_history= medical_history
        patient.status=status
        patient.address = address

        patient.save()
        return redirect('view_patients')

    return render(request,'patients/edit_patients.html')


def add_doctor(request):
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor_name')
        dob = request.POST.get('dob')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        availability = request.POST.get('availability')
        address = request.POST.get('address')

        doctor = Doctor(
            doctor_name=doctor_name,
            date_of_birth=dob,
            specialization=specialization,
            experience=experience,
            age=age,
            phone=phone,
            email=email,
            gender=gender,
            availability=availability,
            address=address,
        )
        doctor.save()
        # Success message or redirection can be added here
        return render(request, 'doctors/add_doctor.html', {'message': 'Doctor added successfully!'})
    else:
        return render(request, 'doctors/add_doctor.html')


def view_doctors(request):
    query = request.GET.get('search', '')
    if query:
        doctors = Doctor.objects.filter(
            Q(doctor_name__icontains=query) | Q(specialization__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()

    context = {'doctors': doctors}
    return render(request, 'doctors/view_doctors.html', context)


def edit_doctors(request,id):
    doctor = Doctor.objects.filter(id=id)

    context = {
        'doctor': doctor,
    }
    return render(request, 'doctors/edit_doctors.html', context)

def update_doctor(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        doctor_name = request.POST.get('doctor_name')
        dob = request.POST.get('dob')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        availability = request.POST.get('availability')
        address = request.POST.get('address')

        doctor=Doctor.objects.get(id=doctor_id)
        doctor.doctor_name=doctor_name
        doctor.date_of_birth = dob
        doctor.age = age
        doctor.phone = phone
        doctor.email = email
        doctor.gender = gender
        doctor.specialization=specialization
        doctor.experience=experience
        doctor.availability= availability
        doctor.address = address

        doctor.save()
        return redirect('view_doctors')

    return render(request,'doctors/edit_doctors.html')

def delete_doctor(request, doctor_id):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        doctor.delete()
        return redirect('view_doctors')
    else:
        return HttpResponseForbidden()


def add_appointment(request):
    if request.method == 'POST':
        # Get appointment data from form
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')  # Optional, depending on form design
        department = request.POST.get('department')
        doctor_name = request.POST.get('doctor_name')
        date1 = request.POST.get('date1')
        email=request.POST.get('email')
        time_slot = request.POST.get('time_slot')
        status = request.POST.get('status')  # Optional, depending on initial status
        problem = request.POST.get('problem')

        # Create and save Appointment object
        appointment = Appointment(
            patient_id=patient_id,
            patient_name=patient_name,  # Optional, depending on form design
            department=department,
            doctor_name=doctor_name,
            date1=date1,
            email=email,
            time_slot=time_slot,
            status=status,  # Optional, depending on initial status
            problem=problem
        )
        appointment.save()

    # Render the add_appointment.html template (replace with your actual template name)
    return render(request, 'appointments/add_appointment.html')

def view_appointments(request):
    query = request.GET.get('search','')  # Get search query from URL parameters
    if query:
        appointments = Appointment.objects.filter(
            Q(patient_name__icontains=query) | Q(doctor_name__icontains=query)
        )  # Filter by patient or doctor name
    else:
        appointments = Appointment.objects.all()  # Get all appointments

    context = {'appointments': appointments}
    return render(request, 'appointments/view_appointments.html', context)


def update_appointment(request):
    if request.method == 'POST':
        # Get updated appointment data from the form
        appointment_id = request.POST.get('appointment_id')
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')  # Optional, depending on form design
        department = request.POST.get('department')
        doctor_name = request.POST.get('doctor_name')
        date1 = request.POST.get('date1')
        email = request.POST.get('email')
        time_slot = request.POST.get('time_slot')
        status = request.POST.get('status')  # Optional
        problem = request.POST.get('problem')

        appointment = Appointment.objects.get(id=appointment_id)
        # Update appointment object with new data
        appointment.patient_id = patient_id
        appointment.patient_name = patient_name  # Optional
        appointment.department = department
        appointment.doctor_name = doctor_name
        appointment.date1 = date1
        appointment.email=email
        appointment.time_slot = time_slot
        appointment.status = status  # Optional
        appointment.problem = problem

        appointment.save()


        # Redirect to a confirmation page or view_appointments after successful update
        return redirect('view_appointments')  # Replace with your desired redirection

    return render(request, 'appointments/edit_appointment.html')


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        appointment.delete()
        return redirect('view_appointments')  # Redirect to view_appointments after deletion

    return HttpResponseForbidden()  # Return forbidden response for GET requests (optional)


def edit_appointment(request,id):
    appointment = Appointment.objects.filter(id=id)

    context = {
        'appointment': appointment,
    }
    return render(request, 'appointments/edit_appointment.html', context)


def add_payment(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')
        doctor_name = request.POST.get('doctor_name')
        admission_date = request.POST.get('admission_date')
        discharge_date = request.POST.get('discharge_date')
        room_charge = request.POST.get('room_charge')  # Assuming it's an integer
        doctor_fee = request.POST.get('doctor_fee')  # Assuming it's an integer
        medicine_cost = request.POST.get('medicine_cost')  # Assuming it's an integer
        other_charge = request.POST.get('other_charge')  # Assuming it's an integer

        # Create and save Payment object
        payment = Payment(
            patient_id=patient_id,
            patient_name=patient_name,
            doctor_name=doctor_name,
            admission_date=admission_date,
            discharge_date=discharge_date,
            room_charge=room_charge,
            doctor_fee=doctor_fee,
            medicine_cost=medicine_cost,
            other_charge=other_charge
        )
        payment.save()
    return render(request, 'payments/add_payments.html')


def view_payment(request):
    search_query = request.GET.get('search', '')  # Get search query from URL parameters
    # Filter payments based on the search query
    if search_query:
        payments = Payment.objects.filter(patient_name__icontains=search_query)
    else:
        payments = Payment.objects.all()
        for payment in payments:
            payment.total = (
                    payment.room_charge +
                    payment.doctor_fee +
                    payment.medicine_cost +
                    payment.other_charge
            )
    context = {'payments': payments}
    return render(request, 'payments/view_payment.html', context)


def delete_payment(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    if request.method == 'POST':
        payment.delete()
        return redirect('view_payment')  # Redirect to view_payments after deletion
    else:
        return HttpResponseForbidden()

def edit_payment(request,id):
    payment = Payment.objects.filter(id=id)

    context = {
        'payment': payment,
    }
    return render(request, 'payments/edit_payment.html', context)


def update_payment(request):
    if request.method == 'POST':
        # Get updated payment data from the form
        patient_id = request.POST.get('patient_id')
        patient_name = request.POST.get('patient_name')
        doctor_name = request.POST.get('doctor_name')
        admission_date = request.POST.get('admission_date')
        discharge_date = request.POST.get('discharge_date')
        room_charge = request.POST.get('room_charge')  # Assuming it's an integer
        doctor_fee = request.POST.get('doctor_fee')  # Assuming it's an integer
        medicine_cost = request.POST.get('medicine_cost')  # Assuming it's an integer
        other_charge = request.POST.get('other_charge')  # Assuming it's an integer
        payment_id=request.POST.get('payment_id')
        payment = Payment.objects.get(id=payment_id)
        # Update payment object with new data
        payment.patient_id = patient_id
        payment.patient_name = patient_name
        payment.doctor_name = doctor_name
        payment.admission_date = admission_date
        payment.discharge_date = discharge_date
        payment.room_charge = room_charge
        payment.doctor_fee = doctor_fee
        payment.medicine_cost = medicine_cost
        payment.other_charge = other_charge

        payment.save()

        # Redirect to a confirmation page or view_payments after successful update
        return redirect('view_payment')  # Replace with your desired redirection

    return render(request, 'payments/view_payment.html')

def generate_payment_bill(request, payment_id):
    try:
        payment = Payment.objects.get(pk=payment_id)


        # Render the HTML template
        html_string = render_to_string('payment_template.html', {'payment': payment})

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="payment_{payment_id}_bill.pdf"'

        # Convert HTML to PDF
        pisa_status = pisa.CreatePDF(
            html_string, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF: %s' % pisa_status.err)

        return response

    except Payment.DoesNotExist:
        return HttpResponse("Payment not found.")


def send_reminder(request, appointment_id):
    if request.method == "POST":
        # Get the appointment object
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # Check if the appointment has a related patient email
        try:
            patient_email = appointment.email  # Adjust field/relationship as per your models
        except AttributeError:
            return redirect('home')  # Replace 'home' with the correct URL name

        # Construct email content
        subject = "Appointment Reminder"
        message = (
            f"Dear {appointment.patient_name},\n\n"
            f"This is a reminder for your appointment with Dr. {appointment.doctor_name} "
            f"on {appointment.date1} at {appointment.time_slot}.\n\n"
            "Please let us know if you have any questions.\n\n"
            "Thank you,\nPro Clinic"
        )
        from_email = "gouthamkr00@gmail.com"  # Replace with your clinic's email


        # Send the email
        send_mail(subject, message, from_email, [patient_email])



        # Redirect back to the same page
        return redirect('home')  # Replace 'home' with the name of your homepage or dashboard view

    # If the request is not POST, redirect back to home
    return redirect('home')  # Replace 'home' with the correct URL name

def export_appointments_csv(request):
    query = request.GET.get('search', '')
    appointments = Appointment.objects.filter(
        Q(patient_name__icontains=query) | Q(doctor_name__icontains=query)
    ) if query else Appointment.objects.all()

    field_names = ['id', 'patient_id', 'patient_name', 'department',
                   'doctor_name', 'date1', 'time_slot', 'problem', 'status']
    column_headers = ['Appointment ID', 'Patient ID', 'Patient Name',
                      'Department', 'Doctor Name', 'Date', 'Time Slot',
                      'Problem', 'Status']

    return export_to_csv(appointments, 'appointments', field_names, column_headers)


# PDF Export View for Appointments
def export_appointments_pdf(request):
    query = request.GET.get('search', '')
    appointments = Appointment.objects.filter(
        Q(patient_name__icontains=query) | Q(doctor_name__icontains=query)
    ) if query else Appointment.objects.all()

    field_names = ['id', 'patient_id', 'patient_name', 'department',
                   'doctor_name', 'date1', 'time_slot', 'problem', 'status']
    column_headers = ['Appointment ID', 'Patient ID', 'Patient Name',
                      'Department', 'Doctor Name', 'Date', 'Time Slot',
                      'Problem', 'Status']

    return export_to_pdf(appointments, 'appointments', field_names, column_headers)

def export_doctors_csv(request):
    search_query = request.GET.get('search', '')
    doctors = Doctor.objects.filter(doctor_name__icontains=search_query)

    field_names = ['id', 'doctor_name', 'experience', 'phone', 'specialization', 'availability']
    column_headers = ['Doctor ID', 'Doctor Name', 'Experience (Years)', 'Phone', 'Specialization', 'Availability']

    return export_to_csv(doctors, 'doctors_list', field_names, column_headers)


# Export Doctors PDF
def export_doctors_pdf(request):
    search_query = request.GET.get('search', '')
    doctors = Doctor.objects.filter(doctor_name__icontains=search_query)

    field_names = ['id', 'doctor_name', 'experience', 'phone', 'specialization', 'availability']
    column_headers = ['Doctor ID', 'Doctor Name', 'Experience (Years)', 'Phone', 'Specialization', 'Availability']

    return export_to_pdf(doctors, 'doctors_list', field_names, column_headers)

def export_patients_csv(request):
    search_query = request.GET.get('search', '')
    patients = Patient.objects.filter(patient_name__icontains=search_query)

    field_names = ['id', 'patient_name', 'age', 'phone', 'date_of_birth', 'gender', 'medical_history', 'status']
    column_headers = ['Patient ID', 'Patient Name', 'Age', 'Phone', 'Date of Birth', 'Gender', 'Medical History', 'Status']

    return export_to_csv(patients, 'patients_list', field_names, column_headers)


# Export Patients to PDF
def export_patients_pdf(request):
    search_query = request.GET.get('search', '')
    patients = Patient.objects.filter(patient_name__icontains=search_query)

    field_names = ['id', 'patient_name', 'age', 'phone', 'date_of_birth', 'gender', 'medical_history', 'status']
    column_headers = ['Patient ID', 'Patient Name', 'Age', 'Phone', 'Date of Birth', 'Gender', 'Medical History', 'Status']

    return export_to_pdf(patients, 'patients_list', field_names, column_headers)



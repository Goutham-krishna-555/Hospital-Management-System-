🏥 Hospital Management System (HMS)

This project implements a Hospital Management System using Django with SQLite3. The HMS offers a comprehensive suite of features to streamline various hospital operations, including:

👩‍⚕️ Patient Management

Add, edit, and search patient records.
Track patient medical history, personal details, treatment plans, and health status.

👨‍⚕️ Doctor and Staff Management

Manage doctor profiles, including specialties, availability, and scheduling.
Ensure proper coordination for appointments and patient care.

📅 Appointment and Scheduling

Automate appointment scheduling.
Track upcoming visits and send reminders.
Avoid overbooking and improve patient and doctor coordination.

💰 Billing and Financial Management

Manage the billing process.
Track patient payments and generate invoices.
Ensure accurate tracking of medical costs, insurance details, and payment histories.

📊 Reporting and Data Analysis

Generate reports on patient visits, treatments, billing, and overall hospital performance.
Provide data visualizations and analytical tools for insights into hospital operations and improved service delivery.

🔒 Security and Backup

Ensure security of sensitive medical data through encryption and restricted access controls.
Include daily backups and data recovery mechanisms to prevent data loss.

⚙️ Technologies Used

🌐 Django Framework

High-level Python web framework for rapid development and clean design, well-suited for database-driven applications like HMS.

📋 SQLite3 Database

Lightweight, serverless, self-contained database engine for easy setup and ideal for small to medium-sized applications.

🔄 Django ORM (Object-Relational Mapping)

Simplifies database interaction using Python objects for creating, retrieving, updating, and deleting records.

📈 Matplotlib

Popular Python library for data visualization, creating charts and reports based on hospital performance metrics.

📄 xhtml2pdf

Converts HTML pages into PDF documents for generating printable bills and reports.

📧 Django Email Integration

Send email reminders for appointments, billing alerts, and other notifications directly from the application.

⏰ Python's datetime and timedelta

Handle dates and times for scheduling appointments, calculating follow-up dates, and sending reminders.

📂 CSV Library

Export patient visit data, appointments, and payment histories into CSV files for reporting and data analysis.

💬 Django Messages Framework

Display success or error messages to the user for feedback on actions performed.

🛡️ Security Best Practices

Implement secure settings to prevent common attacks and ensure secure storage and transmission of sensitive data.

📂 Modules

🏠 Home

Provides an overview of key hospital metrics and data with interactive visualizations using Matplotlib.

👩‍⚕️ Patient

Manage patient information, including adding, viewing, editing, and deleting records.

👨‍⚕️ Doctor

Manage doctor information, including adding, viewing, editing, and deleting profiles.

📅 Appointment

Schedule appointments.

View upcoming and past appointments.

Edit and update appointment details.

Send email reminders.

💰 Payment

Manage financial transactions:

Record payments.

View past payments.

Edit and delete payment records.

Generate bills.

🔔 Reminder

Send automated email reminders to patients about upcoming appointments.

📤 Export Appointments to CSV/PDF

Export appointment data to CSV or PDF formats for reporting and archiving purposes.

This HMS application offers a robust and user-friendly solution for managing various aspects of a hospital, improving operational efficiency, and enhancing patient care.


in the settings.py you have to add ur own email and password

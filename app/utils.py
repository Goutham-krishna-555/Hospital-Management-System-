import csv
from django.http import HttpResponse, FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import io


# CSV Export Function
def export_to_csv(queryset, filename, field_names, column_headers):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(column_headers)

    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        writer.writerow(row)

    return response


# PDF Export Function

def calculate_col_widths(data, max_width=500):
    """
    Calculate column widths dynamically based on data length.
    """
    num_cols = len(data[0])
    max_text_widths = [0] * num_cols

    for row in data:
        for i, cell in enumerate(row):
            cell_width = canvas.Canvas("temp").stringWidth(str(cell), "Helvetica", 8)
            max_text_widths[i] = max(max_text_widths[i], cell_width + 10)

    # Normalize widths to fit within max_width
    total_width = sum(max_text_widths)
    if total_width > max_width:
        scaling_factor = max_width / total_width
        max_text_widths = [width * scaling_factor for width in max_text_widths]

    return max_text_widths


def export_to_pdf(queryset, filename, field_names, column_headers):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []

    # Prepare table data
    data = [column_headers]
    for obj in queryset:
        row = [getattr(obj, field) for field in field_names]
        data.append(row)

    # Calculate column widths dynamically
    col_widths = calculate_col_widths(data)

    # Create table
    table = Table(data, colWidths=col_widths)

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Adjust font size if needed
    ]))

    elements.append(table)
    doc.build(elements)

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'{filename}.pdf')

# hospital/utils.py

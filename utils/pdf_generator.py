from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_pdf(patient, output_dir):
    """Generate a patient report PDF"""
    patient_id, name, age, gender, diagnosis = patient
    filename = f"{name.replace(' ', '_')}.pdf"
    pdf_path = os.path.join(output_dir, filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, f"Patient ID: {patient_id}")
    c.drawString(100, 730, f"Name: {name}")
    c.drawString(100, 710, f"Age: {age}")
    c.drawString(100, 690, f"Gender: {gender}")
    c.drawString(100, 670, f"Diagnosis: {diagnosis}")
   
    c.save()

    return pdf_path

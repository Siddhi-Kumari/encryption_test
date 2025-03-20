from PyPDF2 import PdfWriter, PdfReader
import os

def encrypt_pdf(pdf_path, password, output_dir):
    encrypted_pdf_path = os.path.join(output_dir, os.path.basename(pdf_path))

    writer = PdfWriter()
    reader = PdfReader(pdf_path)

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open(encrypted_pdf_path, "wb") as encrypted_file:
        writer.write(encrypted_file)

    return encrypted_pdf_path


import os
from rlextra.utils.pdfencrypt import encryptPdfOnDisk

def encrypt_pdf(pdf_path, owner_password, output_dir):
    """Encrypt PDF with owner-level security using rlextra."""
    encrypted_pdf_path = os.path.join(output_dir, os.path.basename(pdf_path))
    
    try:
        encryptPdfOnDisk(
            inputFileName=pdf_path,  # Corrected argument name
            outputFileName=encrypted_pdf_path,  # Corrected argument name
            userPassword="",
            ownerPassword=owner_password,
            canPrint=0,
            canModify=0,
            canCopy=0,
            canAnnotate=0
        )
        print(f"✅ PDF encrypted successfully: {encrypted_pdf_path}")
        return encrypted_pdf_path
    except Exception as e:
        print(f"❌ Error encrypting PDF: {e}")
        return None  

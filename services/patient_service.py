import os
from database.db_config import get_db_connection
from utils.password_generator import generate_password
from utils.pdf_generator import create_pdf
from utils.pdf_encryptor import encrypt_pdf
from utils.hash_generator import generate_sha256

# Define directories
BASE_DIR = "E:\\encryption_test"
PATIENT_DIR = os.path.join(BASE_DIR, "patient_reports")
ENCRYPTED_DIR = os.path.join(BASE_DIR, "encrypted_reports")

# Ensure directories exist
os.makedirs(PATIENT_DIR, exist_ok=True)
os.makedirs(ENCRYPTED_DIR, exist_ok=True)

def fetch_patients():
    """Fetches patients from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, gender, diagnosis FROM patients")
    patients = cursor.fetchall()
    conn.close()
    
    return patients

def process_patient_report(patient):
    """Processes a single patient: generates and encrypts PDF, stores password."""
    patient_id, name, age, gender, diagnosis = patient
    password = generate_password()
    
    pdf_path = create_pdf((patient_id, name, age, gender, diagnosis, password, ""), PATIENT_DIR)
    sha256_hash = generate_sha256(pdf_path)
    
    encrypted_pdf_path = encrypt_pdf(pdf_path, password, ENCRYPTED_DIR)
    
    # Debugging prints
    print(f"Generated password for {name}: {password}")
    print(f"SHA256 Hash for {name}: {sha256_hash}")

    # Store password and hash in the database
    conn = get_db_connection()
    if conn is None:
        print("Error: Database connection failed!")
        return

    cursor = conn.cursor()
    update_query = """
        UPDATE patients SET pdf_password = %s, sha256_hash = %s WHERE id = %s
    """
    
    try:
        cursor.execute(update_query, (password, sha256_hash, patient_id))
        conn.commit()
        print(f"✅ Database updated for {name} (ID: {patient_id})")
    except Exception as e:
        print(f"❌ Database update failed for {name}: {e}")
    finally:
        conn.close()

    print(f"Processed report for {name}: {encrypted_pdf_path}")


def process_patient_reports():
    """Processes all patients in the database."""
    print("Processing patient reports...")
    patients = fetch_patients()
    for patient in patients:
        process_patient_report(patient)

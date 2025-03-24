import os
from database.db_config import get_db_connection
from utils.password_utils import hash_password, verify_password
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
    """Fetch patients from the database."""
    conn = get_db_connection()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age, gender, diagnosis FROM patients")
    patients = cursor.fetchall()
    conn.close()
    
    return patients

def process_patient_report(patient):
    """Process a single patient: generates and encrypts PDF, stores password securely."""
    patient_id, name, age, gender, diagnosis = patient
    print(f"\n📂 Processing report for {name} (ID: {patient_id})...")
    password = generate_password()
    hashed_password = hash_password(password)

    pdf_path = create_pdf((patient_id, name, age, gender, diagnosis), PATIENT_DIR)
    print(f"📄 PDF generated at {pdf_path}")
    encrypted_pdf_path = encrypt_pdf(pdf_path, password, ENCRYPTED_DIR)
    print(f"🔐 Encrypted PDF stored at {encrypted_pdf_path}")

    # Generate hash after encryption
    sha256_hash = generate_sha256(encrypted_pdf_path)
    print(f"🔑 SHA256 Hash: {sha256_hash}") 

    # Store hashed password and hash in the database
    conn = get_db_connection()
    if conn is None:
        print("❌ Database connection failed!")
        return

    cursor = conn.cursor()
    update_query = """
        UPDATE patients SET pdf_password = %s, sha256_hash = %s WHERE id = %s
    """
    
    try:
        cursor.execute(update_query, (hashed_password, sha256_hash, patient_id))
        conn.commit()
        print(f"✅ Database updated for {name} (ID: {patient_id})")
    except Exception as e:
        print(f"❌ Database update failed for {name}: {e}")
    finally:
        conn.close()

    print(f"Processed report for {name}: {encrypted_pdf_path}")

def process_patient_reports():
    """Process all patients in the database."""
    print("Processing patient reports...")
    patients = fetch_patients()
    for patient in patients:
        process_patient_report(patient)

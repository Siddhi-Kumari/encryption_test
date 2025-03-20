from db_config import get_db_connection



def setup_database():
    """Create the patients table if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            pdf_password TEXT NOT NULL,
            sha256_hash TEXT
        );
    ''')
    
    conn.commit()
    conn.close()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_database()

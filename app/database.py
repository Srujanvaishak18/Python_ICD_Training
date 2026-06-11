import oracledb
import os

# Database configuration
DB_CONFIG = {
    "user": "SYSTEM",
    "password": "newpassword",
    "dsn": "localhost:1521/XE"
}

def get_db_connection():
    """Create and return Oracle database connection"""
    try:
        oracledb.init_oracle_client(lib_dir=r"C:\instantclient_23_0")
        conn = oracledb.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def verify_connection():
    """Verify database connection on startup"""
    conn = get_db_connection()
    if conn:
        print("✅ Database connected successfully!")
        conn.close()
        return True
    else:
        print("❌ Database connection failed!")
        return False
import mysql.connector
import config

def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

def log_delivery(message_id, telco_partner, reference_number, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sms_delivery_log (message_id, telco_partner, reference_number, status)
        VALUES (%s, %s, %s, %s)
    """, (message_id, telco_partner, reference_number, status))
    conn.commit()
    cursor.close()
    conn.close()


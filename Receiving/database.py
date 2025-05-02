import mysql.connector
import config

def get_connection():
    """Return a new MySQL connection."""
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

def fetch_pending_messages(limit=config.FETCH_BATCH_SIZE):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM sms_messages
        WHERE status = 'PENDING'
        ORDER BY id ASC
        LIMIT %s
    """, (limit,))
    messages = cursor.fetchall()
    if messages:
        ids = [str(msg['id']) for msg in messages]
        cursor.execute(f"""
            UPDATE sms_messages
            SET status = 'PROCESSING'
            WHERE id IN ({",".join(ids)})
        """)
    conn.commit()
    cursor.close()
    conn.close()
    return messages

def update_message_status(message_id, new_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE sms_messages
        SET status = %s
        WHERE id = %s
    """, (new_status, message_id))
    conn.commit()
    cursor.close()
    conn.close()


import socket
import time
import config
import database
import logging

def process_message(message):
    """
    Sends a message in the format:
       id|mobile|message_body
    Expects a response from the gateway (e.g. "Id=12345|Mob=94771234567").
    Updates the database status based on the outcome.
    """
    message_id = message['id']
    mobile = message['mobile']
    message_body = message['message_body']
    data_to_send = f"{message_id}|{mobile}|{message_body}".encode('utf-8')
    
    logging.info(f"Processing message {message_id} for mobile {mobile}")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((config.GATEWAY_SERVER_IP, config.GATEWAY_SERVER_PORT))
            s.sendall(data_to_send)
            
            response = s.recv(1024).decode('utf-8').strip()
            logging.info(f"Received response: {response} for message {message_id}")
            
            if "Id=0" in response:
                database.update_message_status(message_id, 'FAILED')
                logging.error(f"Message {message_id} delivery failed. Response: {response}")
            else:
                database.update_message_status(message_id, 'DELIVERED')
                logging.info(f"Message {message_id} delivered successfully.")
    except Exception as e:
        logging.exception(f"Exception processing message {message_id}: {e}")
        database.update_message_status(message_id, 'FAILED')

def worker_loop():
    """Continuously fetch and process pending messages."""
    while True:
        messages = database.fetch_pending_messages()
        if not messages:
            time.sleep(2)
            continue
        for msg in messages:
            process_message(msg)

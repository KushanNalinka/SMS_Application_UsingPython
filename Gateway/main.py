import socket, threading, logging
import config, database
from logger import setup_logger
from telco_partner import send_via_telco

def handle_client_connection(conn, addr):
    try:
        raw = conn.recv(1024).decode().strip()
        logging.info(f"From {addr} → {raw}")
        parts = raw.split('|', 2)
        if len(parts) != 3:
            conn.sendall(b"Id=0|Invalid format")
            return

        mid, mobile, body = parts
        msg_ref, partner = send_via_telco(mobile, body)

        if msg_ref:
            database.log_delivery(mid, partner, msg_ref, "DELIVERED")
            resp = f"Id={msg_ref}|Mob={mobile}"
            logging.info(f"{mid} → DELIVERED via {partner} ref={msg_ref}")
        else:
            database.log_delivery(mid, partner, '0', "FAILED")
            resp = f"Id=0|Mob={mobile}"
            logging.error(f"{mid} → FAILED via {partner}")

        conn.sendall(resp.encode())
    except Exception as e:
        logging.exception("Error in handler")
        conn.sendall(b"Id=0|Error")
    finally:
        conn.close()

def start_gateway():
    sock = socket.socket()
    sock.bind((config.HOST, config.PORT))
    sock.listen(5)
    logging.info(f"Gateway listening on {config.HOST}:{config.PORT}")
    while True:
        conn, addr = sock.accept()
        threading.Thread(target=handle_client_connection,
                         args=(conn,addr), daemon=True).start()

def main():
    setup_logger()
    start_gateway()

if __name__ == "__main__":
    main()

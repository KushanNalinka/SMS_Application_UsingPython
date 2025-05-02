# sms_gateway_server/telco_partner.py

import logging
from smpplib.client import Client
from smpplib import consts
import config

class TelcoClient:
    def __init__(self, name, host, port, system_id, password, bind_type):
        self.name      = name
        self.host      = host
        self.port      = port
        self.system_id = system_id
        self.password  = password
        self.bind_type = bind_type  # 'transmitter' or 'transceiver'
        self.session   = None

    def connect_and_bind(self):
        logging.info(f"{self.name}: connecting to {self.host}:{self.port}")
        try:
            sess = Client(self.host, self.port)
            sess.connect()
            if self.bind_type == 'transmitter':
                sess.bind_transmitter(
                    system_id=self.system_id,
                    password=self.password
                )
                logging.info(f"{self.name}: bound as transmitter")
            else:
                sess.bind_transceiver(
                    system_id=self.system_id,
                    password=self.password
                )
                logging.info(f"{self.name}: bound as transceiver")
            self.session = sess
        except Exception as e:
            logging.exception(f"{self.name}: bind failed — {e}")
            self.session = None

    def send_sms(self, mobile, message):
        # Ensure session is (re)bound
        if self.session is None:
            self.connect_and_bind()
            if self.session is None:
                return None

        try:
            pdu = self.session.send_message(
                source_addr_ton       = consts.TON_ALPHANUMERIC,
                source_addr           = self.system_id,
                dest_addr_ton         = consts.TON_INTERNATIONAL,
                dest_addr             = mobile,
                short_message         = message.encode('utf-8'),
                esm_class             = 0,
                registered_delivery   = consts.REGISTERED_DELIVERY_SMSC_RECEIPT,
                data_coding           = consts.ENCODING_DEFAULT,
            )
            return pdu.message_id
        except Exception as e:
            logging.exception(f"{self.name}: send failed — {e}")
            return None

# Instantiate telco clients
dialog   = TelcoClient('Dialog',   **config.DIALOG)
mobitel  = TelcoClient('Mobitel',  **config.MOBITEL)
lankabel = TelcoClient('LankaBel', **config.LANKABEL)

# Bind all at startup
for client in (dialog, mobitel, lankabel):
    client.connect_and_bind()

def send_via_telco(mobile, text):
    """
    Choose primary/fallback based on prefix:
    - 9477 → Dialog first, then Mobitel
    - 9471 → Mobitel first, then Dialog
    - else → Dialog first, then Mobitel
    Returns (message_id, partner_name).
    """
    if mobile.startswith('9477'):
        primary, fallback = dialog, mobitel
    elif mobile.startswith('9471'):
        primary, fallback = mobitel, dialog
    else:
        primary, fallback = dialog, mobitel

    msg_id = primary.send_sms(mobile, text)
    if msg_id:
        return msg_id, primary.name

    # fallback
    msg_id = fallback.send_sms(mobile, text)
    return msg_id, fallback.name


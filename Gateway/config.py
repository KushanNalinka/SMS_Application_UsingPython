# TCP server configuration (for SMS gateway)
HOST = '0.0.0.0'
PORT = 5001

# MySQL configuration for logging delivery (if used)
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'sms_gateway'

# SMPP configuration for each telco partner
DIALOG = {
    'host': '10.58.160.8',
    'port': 2775,
    'system_id': 'boc',
    'password': 'boc123',
    'bind_type': 'trx'
}

MOBITEL = {
    'host': '202.129.234.33',
    'port': 5020,
    'system_id': 'bocHO',
    'password': 'hO#246',
    'bind_type': 'tx'
}

LANKABEL = {
    'host': '119.235.1.79',
    'port': 5019,
    'system_id': 'BOC',
    'password': 'boc@1234',
    'bind_type': 'trx'
}

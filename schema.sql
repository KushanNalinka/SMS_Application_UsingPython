CREATE DATABASE IF NOT EXISTS sms_receiving;
USE sms_receiving;

CREATE TABLE IF NOT EXISTS sms_messages (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mobile VARCHAR(20) NOT NULL,
  message_body VARCHAR(255) NOT NULL,
  status VARCHAR(50) DEFAULT 'PENDING',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO sms_messages (mobile, message_body, status) VALUES
('94771234567','Your OTP is 123456.','PENDING'),
('94711234567','Your balance is Rs.5000','PENDING');

CREATE DATABASE IF NOT EXISTS sms_gateway;
USE sms_gateway;

CREATE TABLE IF NOT EXISTS sms_delivery_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  message_id INT,
  telco_partner VARCHAR(50),
  reference_number VARCHAR(50),
  status VARCHAR(50),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

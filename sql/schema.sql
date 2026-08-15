CREATE DATABASE IF NOT EXISTS client_data_db;
USE client_data_db;

CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_code VARCHAR(50) NOT NULL UNIQUE,
    client_name VARCHAR(150) NOT NULL,
    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL,
    revenue DECIMAL(15,2) NOT NULL DEFAULT 0,
    created_date DATE NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_client_code (client_code),
    INDEX idx_email (email),
    INDEX idx_city (city),
    INDEX idx_state (state),
    INDEX idx_status (status)
);

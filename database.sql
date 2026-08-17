CREATE DATABASE IF NOT EXISTS telecom_db;

USE telecom_db;

-- =========================
-- Plans Table
-- =========================

CREATE TABLE IF NOT EXISTS plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

-- =========================
-- Customers Table
-- =========================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    plan_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (plan_id) REFERENCES plans(plan_id)
);

-- =========================
-- Bills Table
-- =========================

CREATE TABLE IF NOT EXISTS bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    month VARCHAR(20),
    amount DECIMAL(10,2),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- =========================
-- Admin Table
-- =========================

CREATE TABLE IF NOT EXISTS admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- =========================
-- Default Telecom Plans
-- =========================

INSERT INTO plans (plan_name, price)
SELECT 'Basic', 299
WHERE NOT EXISTS (
    SELECT 1 FROM plans WHERE plan_name = 'Basic'
);

INSERT INTO plans (plan_name, price)
SELECT 'Standard', 599
WHERE NOT EXISTS (
    SELECT 1 FROM plans WHERE plan_name = 'Standard'
);

INSERT INTO plans (plan_name, price)
SELECT 'Premium', 999
WHERE NOT EXISTS (
    SELECT 1 FROM plans WHERE plan_name = 'Premium'
);

-- =========================
-- Demo Admin Account
-- =========================

INSERT INTO admin (username, password)
SELECT 'admin', 'admin123'
WHERE NOT EXISTS (
    SELECT 1 FROM admin WHERE username = 'admin'
);
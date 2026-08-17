# Telecom Billing Management System

A full-stack web-based Telecom Billing Management System developed using **Flask, MySQL, Bootstrap, and Chart.js**.

The system provides an admin interface for managing customers, telecom plans, and bills, along with an analytics dashboard for monitoring customer and revenue information.

---

## 📌 Project Overview

The Telecom Billing Management System is designed to simplify basic telecom customer and billing operations through a centralized web application.

The application allows an administrator to:

* Manage customer information
* Assign telecom plans to customers
* Search customers
* Generate and view bills
* Edit and delete customer records
* Monitor customer and plan statistics
* View analytics through an interactive dashboard

---

## 🚀 Features

### 🔐 Admin Authentication

* Admin login system
* Session-based authentication
* Logout functionality

### 👤 Customer Management

* Add new customers
* View customer records
* Edit customer information
* Delete customers
* Search customers by name or phone number
* Automatic customer creation timestamp

### 📱 Telecom Plan Management

* Basic, Standard, and Premium plans
* Plan-price association
* SQL JOIN between customers and plans

### 💰 Billing System

* Generate bills for customers
* Automatically retrieve the customer's plan price
* Store bill information in MySQL
* View generated bills

### 📊 Analytics Dashboard

* Total customer count
* Total number of plans
* Total revenue
* Customer distribution by plan
* Interactive Chart.js visualization

### 🎨 User Interface

* Responsive Bootstrap design
* Dashboard with sidebar navigation
* Professional tables and forms
* Delete confirmation
* Success notifications using Flask flash messages

---

## 🛠️ Technologies Used

| Technology   | Purpose                 |
| ------------ | ----------------------- |
| Python       | Backend programming     |
| Flask        | Web framework           |
| MySQL        | Relational database     |
| HTML5        | Frontend structure      |
| Bootstrap 5  | UI design               |
| Chart.js     | Data visualization      |
| Jinja2       | Dynamic HTML templating |
| Git & GitHub | Version control         |

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │      Web Browser    │
                 │   HTML + Bootstrap  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Flask App      │
                 │    Python Backend   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    MySQL Database   │
                 │                     │
                 │ Customers           │
                 │ Plans               │
                 │ Bills               │
                 │ Admin               │
                 └─────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Chart.js        │
                 │ Analytics Dashboard │
                 └─────────────────────┘
```

---

## 🗄️ Database Structure

The application uses a relational MySQL database named:

```text
telecom_db
```

### Main Tables

#### Customers

```text
customer_id
name
phone
plan_id
created_at
```

#### Plans

```text
plan_id
plan_name
price
```

#### Bills

```text
bill_id
customer_id
month
amount
```

#### Admin

```text
id
username
password
```

The `customers` table is connected to the `plans` table using `plan_id`, while the `bills` table is connected to customers using `customer_id`.

---

## 📂 Project Structure

```text
Telecom-Billing-System/
│
├── app.py
├── README.md
├── .gitignore
│
└── templates/
    ├── home.html
    ├── login.html
    ├── dashboard.html
    ├── customers.html
    ├── add_customer.html
    ├── edit_customer.html
    └── bills.html
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Telecom-Billing-System.git
cd Telecom-Billing-System
```

### 2. Install required Python packages

```bash
pip3 install flask mysql-connector-python
```

### 3. Start MySQL

Make sure MySQL Server is running on your system.

For macOS with Homebrew:

```bash
brew services start mysql
```

### 4. Create the database

Open MySQL:

```bash
mysql -u root -p
```

Then create/select the database:

```sql
CREATE DATABASE telecom_db;
USE telecom_db;
```

Create the required tables according to the database schema used by the application.

### 5. Configure the database connection

Update the MySQL connection settings in `app.py` with your local MySQL credentials.

**Do not upload real passwords or credentials to GitHub.**

### 6. Run the Flask application

```bash
python3 app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

### 7. Open the application

Open the local address in your browser and use the admin login to access the dashboard.

---

## 📊 Dashboard

The dashboard provides an overview of:

* Total customers
* Total plans
* Total revenue
* Customer distribution by telecom plan

Interactive visualizations are implemented using **Chart.js**.

---

## 🔮 Future Enhancements

Planned improvements include:

* Power BI analytics dashboard
* Advanced billing and usage calculation
* PDF bill generation
* REST API integration
* Improved authentication and password security
* Advanced customer analytics
* Revenue trend analysis
* Deployment to a cloud platform

---

## 👨‍💻 Author

**Udit Shah**

B.Tech Computer Science & Engineering

---

## ⭐ Project Highlights

This project demonstrates practical experience with:

* Full-stack web development
* Flask backend development
* MySQL database design
* CRUD operations
* SQL JOIN queries
* Authentication and sessions
* Data visualization
* Responsive web UI
* Git and GitHub version control

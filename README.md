# 🏦 Bank Management System

A simple desktop-based **Bank Management System** developed using **Python and Tkinter**.

The application provides a graphical user interface (GUI) for managing customers, bank accounts, employees, and financial transactions.

---

## ✨ Features

### 🔐 Login System
- Employee login using username and password.
- Supports two employee roles:
  - Admin
  - Employee
- Admin users have access to employee management.

### 👤 Customer Management
- Add new customers.
- Automatically generate Customer IDs.
- Store customer information:
  - Name
  - Phone
  - Email
  - Address
- Display all customers in a table.

### 🏦 Account Management
- Create bank accounts for existing customers.
- Automatically generate Account IDs.
- Support different account types:
  - Savings
  - Checking
- Set an initial balance.
- Display account information including:
  - Account ID
  - Customer ID
  - Account Type
  - Balance
  - Status

### 💰 Transaction Management
The system supports:

- Deposit
- Withdraw
- Transfer

The system also validates:
- Invalid account IDs
- Closed accounts
- Invalid transaction amounts
- Insufficient balance
- Transfers to the same account

### 📋 Transaction History
The application records transactions and displays:
- Transaction ID
- Transaction Type
- Source Account
- Destination Account
- Amount
- Date and Time

### 👥 Employee Management
Admin users can:
- Add employees.
- Create usernames and passwords.
- Assign employee roles.
- View employee information.

---

## 🛠️ Technologies Used

- **Python**
- **Tkinter** – GUI development
- **ttk** – GUI widgets
- **datetime** – Transaction date and time
- **Object-Oriented Programming (OOP)**

---

## 🧱 OOP Concepts Used

The project applies several Object-Oriented Programming concepts, including:

- Classes and Objects
- Encapsulation
- Properties and Setters
- Class Attributes
- Class Methods
- Object Interaction
- Separation of responsibilities between classes

### Main Classes

- `Customer`
- `Bank`
- `Account`
- `Transaction`
- `TransactionManager`
- `BankApp`

---

## 📂 Project Structure

```text
Bank-Management-System/
│
├── bank_gui.py
└── README.md
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/rawanalkomy85/Bank-Management-System.git
```

### 2. Open the project folder

```bash
cd Bank-Management-System
```

### 3. Run the application

```bash
python bank_gui.py
```

> Make sure Python is installed on your computer.

---

## 🔑 Default Login

The application includes a default Admin account for testing:

```text
Username: admin
Password: 1234
```

After logging in as Admin, you can access the employee management section.

> **Note:** This project is for educational purposes, so the login credentials are stored directly in the application code.

---

## 🖥️ Application Sections

### Customers
Manage customer information and view registered customers.

### Accounts
Create and view bank accounts associated with customers.

### Transactions
Perform deposits, withdrawals, transfers, and view transaction history.

### Employees (Admin)
Manage employees and their roles. This section is available only to Admin users.

---

## 👥 Team Members

- **Rawan Mohammed**
- **Sarah Hisham**
- **Basmala Emad**
- **Every Gamil**

---

## 🎓 Project Purpose

This project was developed as an educational project to practice:

- Python programming
- Object-Oriented Programming
- GUI development with Tkinter
- Input validation
- Basic banking system logic
- Git and GitHub

---

## 📌 Notes

- Data is currently stored **in memory** using Python objects and dictionaries.
- Data is not persisted in a database or file after the application is closed.
- The project is intended for learning and demonstration purposes.

## 🚀 Future Improvements

The project can be further improved in future versions by adding:

- Add a feature to delete customer accounts.
- Add a feature to delete employees.
- Improve the GUI design and make the screens more user-friendly.
- Improve the Accounts screen to display updated balances after transactions, especially after transfers.
- Add more validation and error handling.
- Add persistent data storage using a database.

# 🧺 Housing Society Laundry Management System

An open-source desktop application built with **Python Tkinter** to digitally manage laundry services for housing societies. The system provides role-based access for residents, staff, and administrators to efficiently handle laundry orders, tracking, billing, and reporting.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [Default Login Credentials](#default-login-credentials)
- [Project Structure](#project-structure)
- [User Guide](#user-guide)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Team](#team)
- [Support](#support)

---

## 📖 Overview

The **Housing Society Laundry Management System** replaces traditional manual laundry management methods (registers, paper tokens, phone calls) with a reliable, efficient, and transparent digital solution. The system eliminates lost requests, delayed deliveries, billing errors, and lack of transparency.

### Key Benefits:
- ✅ **Reduces manual effort** in placing and tracking orders
- ✅ **Improves accuracy** in billing and service records
- ✅ **Ensures transparency** with real-time order tracking
- ✅ **Provides digital history** of all transactions
- ✅ **Open source & free** for any housing society to use

---

## ✨ Features

### For Residents
- 📝 **Place Laundry Orders** - Select cloth type, quantity, and service (Wash, Iron, Dry Clean)
- 📊 **Track Orders** - Visual progress indicator (pending → received → washing → drying → folded → delivered)
- 💰 **View Bills** - Complete billing history with detailed invoices
- 👤 **User Registration** - Self-registration with flat number

### For Staff
- 📋 **View All Orders** - See all pending and active orders
- 🔄 **Update Order Status** - Double-click to move orders through processing stages
- 👁️ **Real-time Updates** - Changes reflect instantly for residents

### For Admin
- 👥 **User Management** - View and delete residents/staff accounts
- 📊 **Reports Generation** - Daily, Weekly, and Monthly reports
- 📈 **Revenue Tracking** - View total revenue and order statistics
- 🔍 **Complete Oversight** - Monitor all orders and system activity

### General Features
- 🔐 **Role-based Access Control** - Separate dashboards for each user type
- 💾 **SQLite Database** - Lightweight, no external database server required
- 📱 **Desktop Application** - Works offline, no internet required
- 🎨 **User-friendly GUI** - Intuitive interface with Tkinter

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Python Tkinter (built-in) |
| **Database** | SQLite3 (built-in) |
| **Language** | Python 3.6+ |
| **Version Control** | Git & GitHub |
| **License** | MIT Open Source |

**No external dependencies required!** Everything uses Python's standard library.

---

## 📥 Installation

### Prerequisites
- Python 3.6 or higher installed on your system
- Basic knowledge of running Python scripts

### Steps

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/yourusername/laundry-management-system.git
   cd laundry-management-system

📁 Project Structure
laundry-management-system/
│
├── main.py                 # Entry point - launches the application
├── login_window.py         # User authentication & registration
├── resident_dashboard.py   # Resident interface (place orders, track, bills)
├── staff_dashboard.py      # Staff interface (update order status)
├── admin_dashboard.py      # Admin interface (users, reports, monitoring)
├── order_form.py          # Order placement form with pricing
├── order_status.py        # Visual order tracking with progress
├── billing.py             # Invoice generation & payment history
├── database_helper.py     # SQLite database operations
├── utils.py               # Utility functions (validation, formatting)
│
├── laundry_system.db      # SQLite database (auto-created on first run)
└── README.md              # This file


📖 User Guide
For Residents
Registering an Account
Click "New User? Register Here" on the login screen

Fill in your details (Name, Username, Password, Email, Phone, Flat Number)

Select role as "resident" and submit

Login with your new credentials

Placing an Order
From your dashboard, click "📝 Place New Order"

Select cloth type, quantity, and service type

Click "Add Item" - repeat for multiple items

Review total amount and click "Submit Order"

Tracking Orders
Click "📊 Track Orders" from your dashboard

Select an order from the dropdown

View visual status indicator and order details

Viewing Bills
Click "💰 View Bills" from your dashboard

Double-click any order to see detailed invoice

View total spent and pending amounts

For Staff
Updating Order Status
Login as staff member

View all pending and active orders in the table

Double-click on any order to update its status

Status progresses automatically: pending → received → washing → drying → folded → delivered

Click "Refresh" to see updated list

For Admin
Managing Users
Go to "👥 Manage Users" tab

View all registered residents and staff

Select a user and click "Delete User" to remove them (and their orders)

Generating Reports
Go to "📊 Reports" tab

Select report type (Daily, Weekly, Monthly)

Click "Generate Report"

View statistics including:

Total orders

Total revenue

Completed vs pending orders

Detailed order list

Monitoring All Orders
Go to "📋 All Orders" tab

View complete order history across all residents

See order statuses and assigned staff


📄 License
MIT License

Copyright (c) 2026 Shehroz, Tuba, Shehreen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions...

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND...


🙏 Acknowledgments
Python Tkinter community for excellent documentation

SQLite for lightweight database solution

All open-source contributors who inspire collaboration


🔒 Security Note
Passwords are stored using SHA-256 hashing (not plain text)

The database file (laundry_system.db) contains all data

For production use, consider:

Regular database backups

Stronger password policies

Network security if deploying remotely
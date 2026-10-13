# 🛡️ AgentPro — LIC Agent Management System

A professional, modern, and user-friendly web application built with **Python Streamlit** and **Pandas**, designed specifically for LIC (Life Insurance Corporation) agents and managers to streamline client management, policy tracking, premium collections, commission calculations, renewals, claims, and lead conversion.

---

## 🚀 Live Demo & Access
* **Deployed App:** [https://lic-agent-protal-tvq2h9hspwvp86tyeejf2t.streamlit.app/]
* **Access:** Direct access enabled (No login or password required, opens straight to the professional agent dashboard).

---

## ✨ Core Modules & Features

1. **📊 Interactive Dashboard**
   * Real-time metrics tracking Total Clients, Active Policies, Premium Collections, and Commission Totals.
   * Quick-glance summaries and dynamic data tables for recent activities.

2. **👥 Client Management (Full CRUD)**
   * Add, view, update, and manage client records including personal details, addresses, DOB, and nominee relationships.
   * Instant search and filter capabilities across the client directory.

3. **📋 Policy Management**
   * Support for a wide portfolio of LIC policy types: *Endowment Plans, Health Insurance, Money Back Plans, Child Plans, Pension Plans,* and *Term Insurance*.
   * Track policy status (Active, Pending, Lapsed, Matured), Sum Assured, and frequency.

4. **💰 Premium Tracking & 🔔 Renewals**
   * Monitor paid, pending, and overdue premium schedules.
   * Simulate WhatsApp and SMS payment/renewal reminders.

5. **🧮 Commission Calculator**
   * Dynamic calculation of expected agent commissions based on configurable demonstration rates (Year 1: 25%, Year 2: 15%, Years 3–5: 10%, Renewals: 5%).

6. **📝 Claims & 🎯 Lead Management**
   * Track insurance claim submissions and review stages (Under Review, Approved, Rejected).
   * Manage prospective client leads through various pipeline stages.

7. **📈 Reports & Analytics**
   * Generate performance summaries and export client and policy datasets directly to CSV.

---

## 🛠️ Technology Stack
* **Framework:** Python Streamlit
* **Data Processing:** Pandas
* **Styling:** Custom CSS with a professional blue-and-white corporate palette (`#1E40AF` primary, `#3B82F6` secondary, `#F8FAFC` background)

---

## 📦 Project Structure
```text
agentpro-lic/
│
├── app.py                  # Main Streamlit application script
├── requirements.txt        # Python package dependencies
├── .streamlit/
│   └── config.toml         # Theme and UI customization config
└── README.md               # Project documentation# LIC-Agent-Protal

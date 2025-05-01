# Building Management System

## Overview

The Building Management System is a digital platform developed using Django. It manages construction materials on a project site, integrating Africa's Talking APIs to enable material updates and stock checks via USSD and SMS. The system ensures real-time transparency, simple communication, and efficient material tracking among Admins, Supervisors, and Stakeholders.

---

## Features

- Real-time material arrival and usage tracking
- Inventory monitoring via Web, USSD, and SMS
- Automatic SMS notifications for material updates
- Clear user roles (Admin, Supervisor, Stakeholder)
- Simple USSD menu for mobile interaction

---

## User Roles

- **Admin**
  - Full system access
  - Define and manage material types

- **Supervisor**
  - Report daily material usage
  - Register newly arrived materials

- **Stakeholder**
  - View store stock and project history
  - No editing permissions

---

## Africa's Talking Integration

- **USSD** for reporting arrivals and checking store inventory
- **SMS** for automatic material arrival notifications and on-demand inventory updates

---

## System Structure

- **Django Project:** `building_system`
- **App:** `materials`
- **Core Models:**
  - `MaterialType`: Defines material names
  - `MaterialStock`: Tracks available material quantities
  - `ArrivalLog`: Logs materials received
  - `UsageLog`: Logs daily material usage
  - `Stakeholder`: Associates a user as a stakeholder

---

## Web Pages

- **Dashboard:** Overview of stock
- **Register Arrival:** Form to log new material arrivals
- **Register Usage:** Form to log daily material usage
- **View Stock:** Stock overview for stakeholders

---

## USSD Menu Flow

- Welcome Menu:
  1. Report Arrival
  2. View Store Stock

- Report Arrival:
  - Select material -> Enter quantity

- View Stock:
  - List all available materials and their quantities

---

## SMS Commands

- Automatic notification when materials arrive
- Request current stock for specific material or full store overview

---

## Installation & Setup

1. Clone repository:
```bash
git clone <repository-url>
cd building_system
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Apply migrations:
```bash
python manage.py migrate
```

4. Create user roles:
```bash
python manage.py create_groups
```

5. Run server:
```bash
python manage.py runserver
```

---

## Important
- Configure Africa's Talking credentials (`username` and `api_key`) in the environment variables or Django settings.
- Set correct URL endpoints on Africa's Talking for USSD and SMS handling.

---

## License

This project is licensed under the MIT License.

---

## Author

- Developed by [Your Name or Organization]


# Court Management System

A web application that digitalizes court case handling by replacing manual paper records with a centralized database.

Developed for S.Y.B.Sc (Computer Science), Samarth College of Computer Science, Belhe (Savitribai Phule Pune University, 2025-2026).

## Features
- Secure admin login and logout
- Dashboard with total cases, open cases, upcoming hearings and judges
- Register and manage cases (Pending, Hearing, Closed)
- Manage clients, attorneys, judges and courts
- Schedule hearings with a judge, date and type
- Record jury verdicts
- Add, edit and delete records in every section
- Instant search on every list
- Delete protection for records that are still in use
- Sample data loaded automatically on the first run

## Technologies Used
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask (REST API)
- Database: SQLite

## Project Structure
```
court_management/
├── app.py
├── requirements.txt
├── README.md
└── static/
    └── index.html
```

## How to Run
1. Install Python 3.9 or newer
2. Open a terminal in the project folder
3. Install the requirements:
```
   pip install -r requirements.txt
```
4. Start the application:
```
   python app.py
```
5. Open http://127.0.0.1:5000 in your browser

## Default Login
- Username: `admin`
- Password: `admin123`

## Limitations
- Only one admin account
- No document upload, notifications or PDF/Excel reports yet

## Future Enhancements
- Role-based login for clerks, judges and lawyers
- Document upload and hearing reminders
- Report export to PDF and Excel
- MySQL database support

## Author
Korade Nisha Dilip

# Court Management System

A web application that digitalizes court case handling by replacing manual paper records with a centralized database.

Developed for T.Y.B.Sc (Computer Science), Samarth College of Computer Science, Belhe (Savitribai Phule Pune University, 2026-2027).

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




Files Description <br><br>
1. app.py (backend)

This is the main Python file that runs the whole application.
It uses Flask to start the web server on port 5000.
It creates the database and the seven tables (court, judge, attorney, client, cases, hearing, jury) on the first run and adds sample data.
It handles login and logout, and blocks API access for users who are not logged in.
It provides the API routes that add, list, edit and delete records for every table.
It provides the dashboard statistics (total cases, open cases, upcoming hearings, judges).
It serves the frontend page (index.html) when you open the website.
It uses safe SQL queries with ? parameters and a whitelist of table names to prevent SQL injection.

2. court.db (database)

This is the SQLite database file where all your data is stored permanently.
You do not create it by hand. app.py creates it automatically the first time you run the project.
It holds all courts, judges, attorneys, clients, cases, hearings and jury verdicts.
Your data stays in it after you close the app.
To reset the project to the sample data, stop the app, delete this file and run python app.py again.
Do not upload it to GitHub. Add it to .gitignore.

3. requirements.txt

This file lists the Python libraries the project needs.
It contains one line: Flask>=3.0.
Anyone who downloads your project installs everything with one command: pip install -r requirements.txt.
SQLite (sqlite3) is already built into Python, so it does not need to be listed.

Other files in the project

static/index.html: the frontend. It contains the login page, dashboard, tables, forms and search, and it calls the API in app.py.
README.md: the description of the project and the steps to run it, shown on the GitHub page.

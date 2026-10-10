
# Student Query Analytics System

A Python-based web application for recording, managing, and analysing student queries using Streamlit, SQLite, Pandas, and Plotly.

## Overview

The Student Query Analytics System helps organise student queries and provides a dashboard for understanding query patterns, departmental workload, priorities, and resolution progress.

## Features

- Submit student queries through a web form.
- Validate submissions and detect recent duplicate queries.
- Store records in an SQLite database.
- Update query statuses: Pending, In Progress, and Resolved.
- Filter and search submitted queries.
- Visualise query status, categories, departments, and priorities.
- Analyse submission trends over time.
- Calculate resolution rates and resolution durations.

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Git and GitHub

## Getting Started

### Prerequisites

- Python 3 installed
- Git installed

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Jwakoli/student-query-analytics
   ```

2. Navigate into the project directory:

   ```bash
   cd student-query-analytics
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the virtual environment on Windows Command Prompt:

   ```bat
   .venv\Scripts\activate.bat
   ```

5. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

6. Initialise the database:

   ```bash
   python database.py
   ```

7. Launch the application:

   ```bash
   streamlit run app.py
   ```

8. Open the local URL displayed in the terminal.

## Project Structure

```text
student-query-analytics/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
```

## Future Improvements

- Add user authentication and role-based access.
- Add exportable reports.
- Improve analytics with additional performance indicators.
- Add automated tests.
- Deploy the application online.

## Author

Jesse Wanjala Wakoli

Computer Science student interested in data analytics and technology.

## 📸 Application Screenshots

### Analytics Dashboard

![Student Query Analytics Dashboard](screenshots/analytics-dashboard.png)

## 🚀 Getting Started

Follow these steps to run the Student Query Analytics System on your computer.

### Prerequisites

- Python 3.10 or later
- Git
- A web browser

### 1. Clone the repository

```bash
git clone https://github.com/Jwakoli/student-query-analytics.git
cd student-query-analytics
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate demonstration data

```bash
python seed_data.py
```

This creates 30 fictional student-query records for exploring the dashboard. It replaces previously generated sample records while preserving other records in the local database.

### 5. Launch the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL to open in your browser.

## 🧪 Sample Data

The demonstration records are fictional and intended for testing the application's filters, charts, status management, and analytics. They are generated locally and are not included in the GitHub repository's database.

## 🔒 Data and Privacy

The application uses a local SQLite database. Do not enter confidential student information into a public demonstration or share a database containing personal information.

## 👨‍💻 Author

**Jesse Wanjala Wakoli**

- GitHub: [Jwakoli](https://github.com/Jwakoli)
- LinkedIn: [Jesse Wakoli](https://www.linkedin.com/in/jesse-wakoli-a63058380/)
# Salary Management

A full-stack employee salary management application built with **Flask** (backend REST API) and **React** (frontend dashboard).

---

## Features

- **Employee Management** — add, edit, delete, and search employees with server-side pagination
- **Bulk Import** — import up to 10,000+ employees at once from three files (`first_names.txt`, `last_names.txt`, `employee_data.csv`) using streaming + batch inserts
- **Metrics Dashboard** — salary analytics by country, job title, headcount charts, top earners, salary distribution, and average tenure
- **Dark Mode** — toggle between light and dark theme, persisted in `localStorage`

---

## Live Demo

The application is publicly hosted:

| Layer | URL |
|-------|-----|
| Frontend (React) | https://salarymanagementfrontend.vercel.app/ |
| Backend (Flask + Gunicorn) | Render web service |
| Database | PostgreSQL on Render |

---

## Database

| Environment | Engine | Config |
|-------------|--------|--------|
| Development | SQLite | No setup needed — `instance/salary.db` is created automatically on first run |
| Production | PostgreSQL | Set `DATABASE_URL=postgresql://...` in your environment (or `.env` file) |

The hosted deployment has a PostgreSQL database already provisioned on Render. When `DATABASE_URL` is present the app switches to PostgreSQL automatically; when it is absent SQLite is used. See [`.env.example`](.env.example) for the format.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Browser                             │
│              http://localhost:5173                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │           React Frontend (Vite)                  │   │
│  │                                                  │   │
│  │  ┌─────────────┐       ┌──────────────────────┐  │   │
│  │  │ Metrics Tab │       │   Employees Tab      │  │   │
│  │  │             │       │                      │  │   │
│  │  │ • Summary   │       │ • Paginated table    │  │   │
│  │  │   KPI cards │       │ • Server-side search │  │   │
│  │  │ • Charts    │       │ • Add / Edit / Delete│  │   │
│  │  │   (Recharts)│       │ • Bulk import modal  │  │   │
│  │  └─────────────┘       └──────────────────────┘  │   │
│  │                                                  │   │
│  │         Tailwind CSS  •  Dark Mode Toggle        │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │  /api/* proxy                 │
└─────────────────────────┼───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Flask REST API (Python)                    │
│              http://localhost:5000                      │
│                                                         │
│  GET    /health                                         │
│  GET    /employees          (pagination + search)       │
│  POST   /employees                                      │
│  GET    /employees/<id>                                 │
│  PUT    /employees/<id>                                 │
│  DELETE /employees/<id>                                 │
│  POST   /employees/import   (multipart, streaming)      │
│  GET    /employees/metrics  (SQL aggregations)          │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              SQLite Database                            │
│              instance/salary.db                         │
│                                                         │
│  Table: employees                                       │
│  ┌────────┬───────────┬───────────┬─────────┬────────┐  │
│  │ empid  │ full_name │ job_title │ country │ salary │  │
│  │ doj    │ dob       │           │         │        │  │
│  └────────┴───────────┴───────────┴─────────┴────────┘  │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
salary_management/
├── app.py                    # Flask app factory + DB engine selection
├── db.py                     # DBWrapper (SQLite & PostgreSQL), get_db, init_db
├── wsgi.py                   # WSGI entry point for Gunicorn / uWSGI
├── requirements.txt          # Python dependencies
├── .env.example              # Example environment variables (DATABASE_URL)
├── schema/
│   ├── employee.sql          # SQLite table definition
│   └── employee_pg.sql       # PostgreSQL table definition (SERIAL)
├── routes/
│   ├── __init__.py           # blueprint registration
│   ├── health.py             # GET /health
│   └── employee.py           # CRUD + import + metrics
├── tests/
│   ├── test_health.py
│   ├── test_employee.py
│   └── test_employee_import.py
├── frontend/                 # React application
│   ├── index.html
│   ├── vite.config.js        # dev proxy → Flask
│   ├── tailwind.config.js
│   ├── .env.development      # VITE_API_URL for dev
│   ├── .env.production       # VITE_API_URL for prod
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── api/client.js     # all fetch calls (importEmployees, getMetrics, …)
│       ├── hooks/
│       │   ├── useEmployees.js   # pagination, search, AbortController
│       │   ├── useMetrics.js     # metrics fetch with AbortController
│       │   └── useDark.js        # MutationObserver dark-mode hook
│       └── components/
│           ├── layout/           # TabBar
│           ├── employees/        # EmployeesPage, EmployeeTable, EmployeeModal,
│           │                     # ImportModal, SearchBar, Pagination
│           └── metrics/          # MetricsPage, SummaryCards, SalaryByCountryChart,
│                                 # SalaryDistribution, HeadcountChart, TopEarnersTable,
│                                 # SalaryByTitleTable, AvgTenureChart
├── salary-management.postman_collection.json
├── prompt.txt                # all user prompts from the build session
├── first_names.txt           # sample data (10,000 first names)
├── last_names.txt            # sample data (10,000 last names)
└── employee_data.csv         # sample data (10,000 employee rows)
```

---

## Prerequisites

| Requirement | Minimum Version | Notes |
|-------------|-----------------|-------|
| Python | 3.10+ | 3.13 recommended |
| pip3 | any | bundled with Python |
| Node.js | 18+ | required for frontend |
| npm | 9+ | bundled with Node.js |

### Install Python
Download from [python.org](https://www.python.org/downloads/) or via Homebrew:
```bash
brew install python
```

### Install Node.js
Download from [nodejs.org](https://nodejs.org/) or via Homebrew:
```bash
brew install node
```

---

## Installation

### 1. Clone / navigate to the project

```bash
cd salary_management
```

### 2. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

This installs:
- `flask>=3.0` — web framework
- `flask-cors>=4.0` — cross-origin resource sharing for the React dev server

### 3. Install frontend dependencies

```bash
cd frontend
npm install
cd ..
```

This installs React, Vite, Tailwind CSS, Recharts, and related build tools.

---

## Running the Application

Both servers must run at the same time. Open two terminal tabs.

### Terminal 1 — Flask backend

```bash
python3 app.py
```

The API will be available at `http://localhost:5000`.

### Terminal 2 — React frontend

```bash
cd frontend
npm run dev
```

The app will be available at `http://localhost:5173`.

> The Vite dev server proxies all `/api/*` requests to `http://localhost:5000`, so no manual CORS configuration is needed during development.

---

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

43 tests covering health check, all CRUD endpoints, and bulk import (including a 10,000-record stress test).

---

## Bulk Import

To import employees in bulk, use the **Import** button in the Employees tab, or call the API directly:

```bash
curl -X POST http://localhost:5000/employees/import \
  -F "first_names=@first_names.txt" \
  -F "last_names=@last_names.txt" \
  -F "employee_data=@employee_data.csv"
```

Sample files with 10,000 records are included in the project root (`first_names.txt`, `last_names.txt`, `employee_data.csv`).

**File format requirements:**
- `first_names.txt` — one first name per line
- `last_names.txt` — one last name per line (line count must match `first_names.txt`)
- `employee_data.csv` — CSV with headers: `job_title`, `country`, `salary`, `doj`, `dob` (row count must match the name files)

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/employees?page=1&per_page=50&search=` | List employees (paginated + searchable) |
| POST | `/employees` | Create employee |
| GET | `/employees/<id>` | Get employee by ID |
| PUT | `/employees/<id>` | Update employee |
| DELETE | `/employees/<id>` | Delete employee |
| POST | `/employees/import` | Bulk import from files |
| GET | `/employees/metrics` | Aggregated salary analytics |

---

## Note on `prompt.txt`

The file [`prompt.txt`](prompt.txt) at the project root contains every prompt sent during the original development session that produced this codebase. It documents the full conversation-driven build process — from the initial health check API through the React frontend — and serves as a human-readable record of how the application was designed and built incrementally.

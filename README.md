# Campus Management System

A comprehensive web application for managing campus resources, users, and bookings. Built with Django (Backend) and React (Frontend).

## Features

- **User Authentication**: Secure Login and Registration system with role-based access control (Admin, Staff, Student).
- **Resource Management**: Admins and Staff can create, update, and delete campus resources (classrooms, labs, equipment).
- **Booking System**: Users can view available resources and book them for specific time slots.
- **Approval Workflow**: Staff/Admins can approve or reject booking requests.
- **Responsive UI**: Modern, responsive interface built with React.

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: React, Vite, React Router, Axios
- **Database**: SQLite (Default Django DB)

## Folder Structure

```
Campus Management System/
├── backend/            # Django Backend
│   ├── api/            # App for API logic
│   ├── campus_backend/ # Project settings
│   └── manage.py       # Django management script
├── frontend/           # React Frontend
│   ├── src/            # Source code
│   ├── public/         # Static assets
│   └── package.json    # Node dependencies
└── README.md           # Project Documentation
```

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js & npm

### Backend Setup

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    - **Windows**: `venv\Scripts\activate`
    - **macOS/Linux**: `source venv/bin/activate`
4.  Install dependencies:
    ```bash
    pip install django djangorestframework django-cors-headers
    ```
5.  Run migrations:
    ```bash
    python manage.py migrate
    ```
6.  Start the server:
    ```bash
    python manage.py runserver
    ```

### Frontend Setup

1.  Navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```

## API Endpoints

- `POST /api/register/`: User registration
- `POST /api/token/`: User login (JWT)
- `GET /api/resources/`: List all resources
- `POST /api/resources/`: Create a new resource (Admin/Staff only)
- `GET /api/bookings/`: List user bookings
- `POST /api/bookings/`: Create a booking

## Team

- **Python-Team--4**
# AelithraStay BY Oceanne Aminata

AelithraStay is a full-stack Airbnb-style web application built with:

- Frontend: Angular 20 (Standalone Components)
- Backend: Django + Django REST Framework
- Authentication: JWT Authentication
- Database: PostgreSQL or SQLite
- API Communication: REST API

The platform allows users to:

- Register and log in securely
- Browse properties
- Become a host
- Add and manage properties
- Book stays
- Manage reservations
- Upload property images
- Search properties by location

---

# Project Structure

```text
AelithraStay/
│
├── backend/                 # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── aelithrastay/
│   └── apps/
│
├── frontend/                # Angular frontend
│   ├── src/
│   ├── angular.json
│   ├── package.json
│   └── tsconfig.json
│
├── .gitignore
├── README.md
└── docker-compose.yml
```

---

# Technologies Used

## Frontend

- Angular 20
- TypeScript
- RxJS
- Angular Router
- Angular Signals
- Reactive Forms
- Tailwind CSS or SCSS

## Backend

- Django
- Django REST Framework
- Simple JWT
- Django CORS Headers
- Pillow

## Database

- PostgreSQL
- SQLite (Development)

---

# Features

## Authentication

- User registration
- Login system
- JWT access tokens
- Protected routes
- Role-based access (Guest / Host)

## Property Management

- Add properties
- Edit properties
- Delete properties
- Upload property images
- Property listing

## Booking System

- Reserve properties
- Booking management
- Availability handling

## Search & Filtering

- Search by city
- Search by price
- Search by category

---

# Backend Setup (Django)

## 1. Navigate to backend

```bash
cd backend
```

## 2. Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create superuser

```bash
python manage.py createsuperuser
```

## 6. Run Django server

```bash
python manage.py runserver
```

Backend URL:

```text
http://127.0.0.1:8000/
```

---

# Frontend Setup (Angular)

## 1. Navigate to frontend

```bash
cd frontend
```

## 2. Install dependencies

```bash
npm install
```

## 3. Run Angular server

```bash
ng serve
```

Frontend URL:

```text
http://localhost:4200/
```

---

# Angular Development Commands

## Create component

```bash
ng generate component pages/home
```

## Create service

```bash
ng generate service core/auth
```

## Run project

```bash
ng serve
```

## Build production version

```bash
ng build
```

---

# API Authentication

Authentication uses JWT tokens.

## Login Endpoint

```text
POST /api/auth/login/
```

## Register Endpoint

```text
POST /api/auth/register/
```

## Refresh Token Endpoint

```text
POST /api/token/refresh/
```

---

# Environment Variables

## Backend `.env`

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
```

## Frontend Environment

```ts
export const environment = {
  apiUrl: 'http://127.0.0.1:8000/api'
};
```

---

# Git Commands

## Initialize Git

```bash
git init
```

## Add files

```bash
git add .
```

## Commit changes

```bash
git commit -m "Initial commit"
```

## Push to GitHub

```bash
git push -u origin main
```

## Push updates later

```bash
git add .
git commit -m "updated project"
git push
```

---

# Deployment F

## Frontend Deployment

You can deploy Angular on:

- Vercel
- Netlify
- Firebase Hosting

## Backend Deployment

You can deploy Django on:

- Render
- Railway
- PythonAnywhere

---

# Recommended Future Features

- Payment integration (Stripe)
- Real-time chat
- Email verification
- Notifications
- Favorites system
- Reviews and ratings
- Admin dashboard
- Google Maps integration
- Multi-image upload

---

# Screens

- Home Page
- Login Page
- Register Page
- Property Detail Page
- Booking Page
- Host Dashboard
- User Profile

---

# Author

Developed by Oceanne Aminata.

---

# License

This project is for educational and portfolio purposes.


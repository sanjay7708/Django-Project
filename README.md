        Full Stack E-Commerce Web Application
  A full-stack eCommerce web application built using Django REST Framework and React, featuring session-based authentication, product management, cart functionality, and order placement.

Project Overview

This project is a complete eCommerce web application where users can:

Register and log in using session-based authentication

View and browse products

Add products to cart

Modify cart items (increase/decrease quantity or remove)

Place orders

View order details

The backend is built with Django REST Framework, and the frontend is developed using React.
The application uses SQLite as the database and Django ORM for database operations.

✨ Features

User authentication (Session-based login/logout)

Product listing

Add to cart functionality

Update and remove cart items

Order placement

Backend API using Django REST Framework

Secure session handling

Clean and modular code structure

Tech Stack
  Frontend:

    React.js

    HTML

    CSS

    JavaScript

  Backend:

      Python

      Django

      Django REST Framework

  Database:

    SQLite (Django ORM)

📂 Project Structure

Django-Project/
│
├── accounts/          # User authentication and session handling
├── shop/              # Product, cart, and order logic
├── ecomsite/          # Main Django project settings
│
├── media/             # Uploaded media files
├── staticfiles/       # Collected static files
│
├── db.sqlite3         # SQLite database
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
├── runtime.txt        # Runtime environment config
└── README.md

Installation & Setup
  1)Clone the repository
      git clone https://github.com/your-username/ecommerce-project.git

  create virtual environment:
      python -m venv venv
      source venv/bin/activate      # Linux / Mac
      venv\Scripts\activate         # Windows
      
  Install dependencies:
      pip install -r requirements.txt
  2)Backend Setup (Django)
    cd Django-Project
    
      Apply migrations:

      python manage.py makemigrations
      python manage.py migrate


Create superuser:

python manage.py createsuperuser


Run the backend server:

python manage.py runserver


Backend will run at:

http://127.0.0.1:8000/

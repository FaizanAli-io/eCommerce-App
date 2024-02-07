# Django-ECommerce-App

Django Base Code for an E-Commerce Backend.

# Features

- Working API for the User and Product Modules
- A Custom User Class with catgories for Consumers, Vendors, and Admins
- A full suite of unit tests written, following TDD (Test Driven Development)

# Dependencies

- Django
- Django Rest Framework
- DRF Spectacular

# Instructions

- Clone repository: `git clone https://github.com/FaizanAli-io/eCommerce-App.git`

- Change directory: `cd eCommerce-App`

- Create virtual environment: `python -m venv {name of env}`

- Activate virtual environment: `.\{name of env}\Scripts\Activate`

- Install project requirements: `pip install -r .\requirements.txt`

- Run project: `python manage.py runserver 8000`

## Commands

Run server:

```python manage.py runserver { port }```

Create admin user:

```python manage.py createsuperuser```

Run all unit tests:

```python manage.py test```

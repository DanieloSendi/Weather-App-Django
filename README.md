# Weather Application Django
 
## Introduction

Welcome to the **Weather Application Project**, built using **Django - Python Web Framework** for the backend and **HTML | CSS | JS** for the frontend. This application fetches real-time weather data using the **WeatherAPI** and displays it in a user-friendly interface.

---

## Technologies used

- **Backend:** Django
- **Frontend:** HTML, CSS, JS
- **API:** WeatherAPI
- **Database:** PostgreSQL

## Features

- Fetches **real-time weather data** from WeatherAPI  
- Allows users to **search for weather conditions** by city name.
- Displays **weather parameters** such as temperature, humidity, and pressure etc.
- Implements **rate limiting** to prevent API abuse.
- Uses **environment variables** to store API keys and database configuration securely.
- **Handles errors** if the external API is down or if the city name is invalid

## Installation and setup

1. Clone repository:

```bash
git clone https://github.com/DanieloSendi/Weather-App-Django.git
cd Weather-App-Django
```

2. Install and create a virtual environment:

```bash
python -m pip install virtualenv
python -m virtualenv venv
```

3. Activate the virtual environment

```bash
.\venv\Scripts\activate.ps1
```

4. Install dependecies

```bash
pip install -r requirements.txt
```

5. Set up environment variables. Create a .env file in the project root and add the following configuration:

```bash
# API Key for WeatherAPI
API_WEATHER_KEY=your_api_key_here

# PostgreSQL Database Configuration
POSTGRES_DB_NAME=your_database_name
POSTGRES_DB_USER=your_database_user
POSTGRES_DB_PASSWORD=your_database_password
POSTGRES_DB_HOST=your_database_host
POSTGRES_DB_PORT=your_database_port

# Django Secret Key
SECRET_KEY='your_secret_django_key_here'

# Debug Mode
ENVIRONMENT='development'

```

6. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Run locally the development server. Django application is now available at `http://localhost:8000`.

```bash
python manage.py runserver
```

## Deployment (Vercel)

This project can be deployed on **[Vercel](https://vercel.com/home)** using a custom `build.sh` script.  
The script automatically installs dependencies, applies migrations, and collects static files.

Key points:
- `build.sh` handles installation, migration, and static file collection.
- `vercel.json` is configured to use Django as a Python backend server.
- No need to upload `staticfiles/` to GitHub; they are generated during build.

## Future improvemnets
 
- Improve UI design
- Optimize performance with Redis as an in-memory cache to store API responses and reduce redundant requests.
- Add unit tests to ensure application reliability

## Additional Resources

- [Visual Studio Code - Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [Python environments in VS Code](https://code.visualstudio.com/docs/python/environments)
- [Django Web Framework - Documentation](https://docs.djangoproject.com/en/5.1/)
- [Bootstrap - Documentation](https://getbootstrap.com/)
- [WeatherAPI - Documentation](https://www.weatherapi.com/docs/)
- [Icons - Favicon](https://www.freepik.com/)

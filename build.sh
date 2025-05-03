#!/usr/bin/env bash
echo "Starting build script"

# Installation of packages
pip install -r requirements.txt

# Database migration
python3 manage.py makemigrations
python3 manage.py migrate

# Converting static files
python3 manage.py collectstatic --noinput

echo "Build script completed"

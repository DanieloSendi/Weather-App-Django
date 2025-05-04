#!/usr/bin/env bash
echo "Starting build script"

# Exit immediately if a command fails
set -e

# Installation of packages
echo "Installing packages..."
python3 -m pip install -r requirements.txt

# Database migration (apply existing migrations)
echo "Applying database migrations..."
python3 manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Build script completed successfully"

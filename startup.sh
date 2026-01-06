#!/bin/bash

echo "Starting Job Hunter on Azure..."

# Install dependencies
pip install -r requirements.txt

# Create data directory if not exists
mkdir -p data

# Start gunicorn
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers=2 web.app:app
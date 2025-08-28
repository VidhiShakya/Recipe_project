#!/usr/bin/env python
"""
WSGI entry point for Render deployment.
This file ensures the correct Django application is loaded.
"""

import os
import sys
from pathlib import Path

# Add project directory to Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Recipe_project.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Create the WSGI application
application = get_wsgi_application()

if __name__ == "__main__":
    print("WSGI application loaded successfully")
    print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"Project root: {PROJECT_ROOT}")

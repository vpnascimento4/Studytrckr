import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask application
from app import app

# Vercel's @vercel/python runtime automatically detects Flask WSGI applications
handler = app


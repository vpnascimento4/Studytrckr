import sys
import os

# Add parent directory to Python path  
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app
from app import app

# Vercel's @vercel/python runtime automatically detects Flask applications
# The handler must be the Flask app instance
handler = app


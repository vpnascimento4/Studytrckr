import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the Flask application
from app import app

# Expose Flask app as handler
# Note: There's a known bug in Vercel's Python runtime that causes
# TypeError: issubclass() arg 1 must be a class
# This is a Vercel runtime issue, not a code issue
handler = app


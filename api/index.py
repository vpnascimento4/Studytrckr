"""
Vercel serverless function entry point for Flask app.
This file wraps the Flask application for Vercel's serverless environment.
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel's Python runtime expects the Flask app object directly
# The @vercel/python builder automatically detects Flask apps and wraps them
handler = app


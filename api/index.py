"""
Vercel serverless function entry point for Flask app.
This file wraps the Flask application for Vercel's serverless environment.
"""
import sys
import os
import traceback

# Add parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from app import app
    
    # Vercel's Python runtime automatically detects Flask apps
    # The Flask app object is exposed as 'handler'
    # Vercel will automatically wrap it for serverless execution
    handler = app
    
except Exception as e:
    # If import fails, create a simple error handler that shows the error
    error_msg = f"Failed to import Flask app: {str(e)}\n{traceback.format_exc()}"
    print(error_msg)
    
    def handler(request):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/html'},
            'body': f'<h1>Application Error</h1><pre>{error_msg}</pre>'
        }


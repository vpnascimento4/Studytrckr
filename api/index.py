"""
Vercel serverless function entry point for Flask app.
This file wraps the Flask application for Vercel's serverless environment.
"""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    
    # Vercel's Python runtime automatically detects Flask apps
    # The handler should be the Flask app object
    handler = app
    
except Exception as e:
    # Error handling for import/deployment issues
    import traceback
    print(f"Error importing Flask app: {e}")
    traceback.print_exc()
    
    # Create a minimal error handler
    def handler(request):
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'text/plain'},
            'body': f'Application error: {str(e)}'
        }


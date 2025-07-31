import os
from app import app

if __name__ == '__main__':
    # Check if the API key is set
    api_key = os.getenv('SEGMIND_API_KEY')
    fashn_api_key = os.getenv('FASHN_API_KEY')
    
    if not api_key and not fashn_api_key:
        print("Warning: No API key found. Please set SEGMIND_API_KEY or FASHN_API_KEY in your .env file.")
        print("The application will run, but the try-on functionality will not work.")
        print("See API_KEY_GUIDE.md for instructions on how to get an API key.")
    
    # Create necessary directories
    os.makedirs('static/uploads', exist_ok=True)
    os.makedirs('static/results', exist_ok=True)
    
    # Run the Flask application
    app.run(debug=True)

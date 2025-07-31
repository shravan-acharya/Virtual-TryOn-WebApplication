import os
import shutil
import sys

def setup_project():
    """Set up the Virtual Try-On project"""
    print("Setting up the Virtual Try-On project...")
    
    # Create necessary directories
    directories = [
        'static/uploads',
        'static/results',
        'static/img',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from .env.example")
        print("Please edit the .env file to add your API key")
    
    # Check if Python virtual environment exists
    if not os.path.exists('venv'):
        print("\nCreating Python virtual environment...")
        os.system('python -m venv venv')
        print("Virtual environment created")
    
    # Determine the activate script based on the OS
    if sys.platform == 'win32':
        activate_script = 'venv\\Scripts\\activate'
        activate_cmd = f"{activate_script} && pip install -r requirements.txt"
    else:
        activate_script = 'source venv/bin/activate'
        activate_cmd = f"{activate_script} && pip install -r requirements.txt"
    
    print("\nTo complete setup, run the following commands:")
    print(f"1. Activate the virtual environment: {activate_script}")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Edit the .env file to add your API key")
    print("4. Run the application: python run.py")
    
    print("\nOr on Windows, you can run:")
    print(activate_cmd)
    print("python run.py")
    
    print("\nSetup complete!")

if __name__ == "__main__":
    setup_project()

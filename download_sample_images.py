import os
import requests
from PIL import Image
import io

# Create the directory if it doesn't exist
os.makedirs('static/img', exist_ok=True)

# Sample image URLs (these are placeholder URLs - replace with actual URLs if needed)
sample_images = {
    'sample_person.jpg': 'https://storage.googleapis.com/segmind-public/try-on-diffusion/model.png',
    'sample_shirt.jpg': 'https://storage.googleapis.com/segmind-public/try-on-diffusion/cloth.jpg'
}

def download_image(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join('static/img', filename), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename} successfully")
            return True
        else:
            print(f"Failed to download {filename}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {filename}: {str(e)}")
        return False

def create_sample_image(filename, color, size=(300, 400)):
    try:
        img = Image.new('RGB', size, color=color)
        img.save(os.path.join('static/img', filename))
        print(f"Created {filename} successfully")
        return True
    except Exception as e:
        print(f"Error creating {filename}: {str(e)}")
        return False

print("Downloading sample images for testing...")

# Try to download images from URLs
success = True
for filename, url in sample_images.items():
    if not download_image(url, filename):
        success = False

# If downloading fails, create simple colored images
if not success:
    print("\nFallback: Creating simple sample images...")
    create_sample_image('sample_person.jpg', (255, 220, 200))  # Light skin tone color
    create_sample_image('sample_shirt.jpg', (50, 100, 200))    # Blue shirt color

print("\nSample images are ready in the static/img directory.")
print("You can use them with the test scripts:")
print("python test_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg")
print("python debug_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg")

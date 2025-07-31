import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment or use the provided one
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', "1d382b59c4msh374d1f543891f32p106b59jsn93ae938cf161")

def test_multipart_api():
    """Test the RapidAPI Virtual Try-On API using proper multipart/form-data"""
    # Use the sample images from static/img
    model_path = "static/img/sample_person.jpg"
    garment_path = "static/img/sample_shirt.jpg"
    
    # Check if files exist
    if not os.path.exists(model_path):
        print(f"Model image not found at {model_path}")
        return
    
    if not os.path.exists(garment_path):
        print(f"Garment image not found at {garment_path}")
        return
        
    print(f"Using model image: {model_path}")
    print(f"Using garment image: {garment_path}")
    
    # Open the files in binary mode
    with open(model_path, 'rb') as model_file, open(garment_path, 'rb') as garment_file:
        # Prepare the files for the request
        files = {
            'personImage': ('person.jpg', model_file, 'image/jpeg'),
            'clothImage': ('garment.jpg', garment_file, 'image/jpeg')
        }
        
        # Prepare the headers
        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': "virtual-try-on2.p.rapidapi.com"
        }
        
        # Make the request
        url = "https://virtual-try-on2.p.rapidapi.com/clothes-virtual-tryon"
        print("Sending request to RapidAPI...")
        response = requests.post(url, files=files, headers=headers)
        
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            # Check if the response is JSON
            try:
                json_response = response.json()
                print(f"JSON response: {json.dumps(json_response, indent=2)}")
                
                # If it's JSON, it might contain an error message or a URL to the result
                if 'url' in json_response:
                    print(f"Result URL: {json_response['url']}")
                    # Download the image from the URL
                    img_response = requests.get(json_response['url'])
                    if img_response.status_code == 200:
                        with open("multipart_result.jpg", "wb") as f:
                            f.write(img_response.content)
                        print("Result saved as multipart_result.jpg")
                    else:
                        print(f"Failed to download image from URL: {img_response.status_code}")
                else:
                    print("No URL found in JSON response")
            except json.JSONDecodeError:
                # If it's not JSON, it might be the image directly
                print("Response is not JSON, assuming it's the image directly")
                with open("multipart_result.jpg", "wb") as f:
                    f.write(response.content)
                print("Result saved as multipart_result.jpg")
        else:
            print(f"Error: {response.text}")

if __name__ == "__main__":
    test_multipart_api()

import os
import requests
import base64
import argparse
import time
import json
import http.client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', "1d382b59c4msh374d1f543891f32p106b59jsn93ae938cf161")
RAPIDAPI_HOST = "virtual-try-on2.p.rapidapi.com"

def image_to_base64(image_path):
    """Convert an image file to base64 encoding"""
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

def test_rapidapi_tryon(model_image_path, garment_image_path, category=None):
    """Test the RapidAPI Virtual Try-On API"""

    # Read the image files
    try:
        with open(model_image_path, 'rb') as f:
            model_image_data = f.read()

        with open(garment_image_path, 'rb') as f:
            garment_image_data = f.read()
    except Exception as e:
        print(f"Error reading image files: {str(e)}")
        return False

    print("Sending test request to RapidAPI Virtual Try-On...")

    # Method 1: Using requests library with multipart/form-data
    try:
        url = "https://virtual-try-on2.p.rapidapi.com/clothes-virtual-tryon"

        files = {
            'personImage': ('person.jpg', model_image_data, 'image/jpeg'),
            'clothImage': ('garment.jpg', garment_image_data, 'image/jpeg')
        }

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST
        }

        response = requests.post(url, files=files, headers=headers)

        if response.status_code == 200:
            print("Success! API is working correctly.")

            # Save the result image
            result_filename = "api_test_result.jpg"

            with open(result_filename, 'wb') as f:
                f.write(response.content)
            print(f"Result image saved as {result_filename}")
            return True
        else:
            print(f"API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")

            # Try Method 2 if Method 1 fails
            print("Trying alternative method...")
            return test_rapidapi_tryon_alt(model_image_path, garment_image_path)

    except Exception as e:
        print(f"Error making API request: {str(e)}")
        print("Trying alternative method...")
        return test_rapidapi_tryon_alt(model_image_path, garment_image_path)

def test_rapidapi_tryon_alt(model_image_path, garment_image_path):
    """Alternative method to test the RapidAPI Virtual Try-On API using http.client"""
    try:
        # Read the image files
        with open(model_image_path, 'rb') as f:
            model_image_data = f.read()

        with open(garment_image_path, 'rb') as f:
            garment_image_data = f.read()

        conn = http.client.HTTPSConnection("virtual-try-on2.p.rapidapi.com")

        # Create a boundary for multipart form data
        boundary = "---011000010111000001101001"

        # Create a multipart form data payload
        from email.mime.multipart import MIMEMultipart
        from email.mime.image import MIMEImage

        # Create a multipart message
        msg = MIMEMultipart()

        # Add the person image
        person_part = MIMEImage(model_image_data)
        person_part.add_header('Content-Disposition', 'form-data', name="personImage", filename="person.jpg")
        msg.attach(person_part)

        # Add the garment image
        garment_part = MIMEImage(garment_image_data)
        garment_part.add_header('Content-Disposition', 'form-data', name="clothImage", filename="garment.jpg")
        msg.attach(garment_part)

        # Get the payload
        payload = msg.as_string().split('\n\n', 1)[1]

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST,
            'Content-Type': f"multipart/form-data; boundary={boundary}"
        }

        conn.request("POST", "/clothes-virtual-tryon", payload, headers)

        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            print("Success! API is working correctly (alternative method).")

            # Save the result image
            result_filename = "api_test_result.jpg"

            with open(result_filename, 'wb') as f:
                f.write(data)
            print(f"Result image saved as {result_filename}")
            return True
        else:
            print(f"API request failed with status code {res.status}")
            print(f"Response: {data.decode('utf-8')}")
            return False

    except Exception as e:
        print(f"Error making API request (alternative method): {str(e)}")
        return False

def test_fashn_api(model_image_path, garment_image_path, category="tops"):
    """Test the FASHN API"""
    api_key = os.getenv('FASHN_API_KEY')

    if not api_key:
        print("Error: FASHN_API_KEY not found in .env file")
        return False

    url = "https://api.fashn.ai/v1/run"

    # Convert images to base64 or prepare URLs
    try:
        model_image_base64 = image_to_base64(model_image_path)
        garment_image_base64 = image_to_base64(garment_image_path)
    except Exception as e:
        print(f"Error reading image files: {str(e)}")
        return False

    # Prepare the payload (adjust according to FASHN API documentation)
    data = {
        "model_image": model_image_base64,
        "garment_image": garment_image_base64,
        "category": category
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    print("Sending test request to FASHN API...")

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            print("Success! API is working correctly.")

            # Save the result image
            result_filename = "api_test_result.jpg"
            with open(result_filename, 'wb') as f:
                f.write(response.content)

            print(f"Result image saved as {result_filename}")
            return True
        else:
            print(f"API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"Error making API request: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test the Virtual Try-On API')
    parser.add_argument('--api', choices=['rapidapi', 'fashn'], default='rapidapi',
                        help='Which API to test (rapidapi or fashn)')
    parser.add_argument('--model', required=True, help='Path to the model image')
    parser.add_argument('--garment', required=True, help='Path to the garment image')
    parser.add_argument('--category', help='Garment category (only used for FASHN API)')
    parser.add_argument('--alt', action='store_true',
                        help='Use alternative method for RapidAPI')

    args = parser.parse_args()

    if args.api == 'rapidapi':
        if args.alt:
            test_rapidapi_tryon_alt(args.model, args.garment)
        else:
            test_rapidapi_tryon(args.model, args.garment)
    else:
        category = args.category if args.category else "tops"
        test_fashn_api(args.model, args.garment, category)

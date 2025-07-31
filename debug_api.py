import os
import requests
import base64
import argparse
import json
import time
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

def debug_rapidapi_tryon(model_image_path, garment_image_path):
    """Debug the RapidAPI Virtual Try-On API"""

    # Read the image files
    try:
        with open(model_image_path, 'rb') as f:
            model_image_data = f.read()

        with open(garment_image_path, 'rb') as f:
            garment_image_data = f.read()
    except Exception as e:
        print(f"Error reading image files: {str(e)}")
        return

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

        print("Request headers:")
        print(json.dumps(headers, indent=2))

        response = requests.post(url, files=files, headers=headers)

        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")

        if response.status_code == 200:
            print("Success! API is working correctly.")

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")

            # Save the result image
            result_filename = "debug_api_result.jpg"

            # Try to save as binary data
            with open(result_filename, 'wb') as f:
                f.write(response.content)
            print(f"Result image saved as {result_filename}")

            # If it's a text response, print the first 100 characters
            if 'text' in content_type or 'json' in content_type:
                try:
                    print("Response content (first 100 chars):")
                    print(response.text[:100])
                except:
                    pass
        else:
            print(f"API request failed with status code {response.status_code}")
            print(f"Response: {response.text}")

            # Try Method 2 if Method 1 fails
            print("Trying alternative method...")
            debug_rapidapi_tryon_alt(model_image_path, garment_image_path)

    except Exception as e:
        print(f"Error making API request: {str(e)}")
        print("Trying alternative method...")
        debug_rapidapi_tryon_alt(model_image_path, garment_image_path)

def debug_rapidapi_tryon_alt(model_image_path, garment_image_path):
    """Alternative method to debug the RapidAPI Virtual Try-On API using http.client"""
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

        print("Alternative method request headers:")
        print(json.dumps(headers, indent=2))

        conn.request("POST", "/clothes-virtual-tryon", payload, headers)

        res = conn.getresponse()
        data = res.read()

        print(f"Response status code: {res.status}")
        print(f"Response headers: {json.dumps(dict(res.getheaders()), indent=2)}")

        if res.status == 200:
            print("Success! API is working correctly (alternative method).")

            # Save the result image
            result_filename = "debug_api_result_alt.jpg"

            with open(result_filename, 'wb') as f:
                f.write(data)
            print(f"Result image saved as {result_filename}")
        else:
            print(f"API request failed with status code {res.status}")
            print(f"Response: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Error making API request (alternative method): {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Debug the Virtual Try-On API')
    parser.add_argument('--model', required=True, help='Path to the model image')
    parser.add_argument('--garment', required=True, help='Path to the garment image')
    parser.add_argument('--alt', action='store_true',
                        help='Use alternative method (http.client) instead of requests')

    args = parser.parse_args()

    if args.alt:
        debug_rapidapi_tryon_alt(args.model, args.garment)
    else:
        debug_rapidapi_tryon(args.model, args.garment)

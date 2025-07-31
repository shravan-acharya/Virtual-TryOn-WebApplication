import http.client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment or use the provided one
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', "1d382b59c4msh374d1f543891f32p106b59jsn93ae938cf161")

def test_direct_api():
    """Test the RapidAPI Virtual Try-On API using the exact format from their example"""
    import requests

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

    # Read the image files
    with open(model_path, 'rb') as f:
        model_image_data = f.read()

    with open(garment_path, 'rb') as f:
        garment_image_data = f.read()

    # Method 1: Using requests library
    url = "https://virtual-try-on2.p.rapidapi.com/clothes-virtual-tryon"

    files = {
        'personImage': ('person.jpg', model_image_data, 'image/jpeg'),
        'clothImage': ('garment.jpg', garment_image_data, 'image/jpeg')
    }

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "virtual-try-on2.p.rapidapi.com"
    }

    print("Sending request to RapidAPI using requests library...")
    response = requests.post(url, files=files, headers=headers)

    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")

    if response.status_code == 200:
        print("Success! Saving result...")
        with open("requests_result.jpg", "wb") as f:
            f.write(response.content)
        print("Result saved as requests_result.jpg")
    else:
        print(f"Error: {response.text}")

    # Method 2: Using http.client
    conn = http.client.HTTPSConnection("virtual-try-on2.p.rapidapi.com")

    # Use the exact payload format from the example
    payload = "-----011000010111000001101001\r\n"
    payload += "Content-Disposition: form-data; name=\"personImage\"\r\n\r\n"
    payload += "1.jpg\r\n"
    payload += "-----011000010111000001101001\r\n"
    payload += "Content-Disposition: form-data; name=\"clothImage\"\r\n\r\n"
    payload += "2.jpg\r\n"
    payload += "-----011000010111000001101001--\r\n\r\n"

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "virtual-try-on2.p.rapidapi.com",
        'Content-Type': "multipart/form-data; boundary=---011000010111000001101001"
    }

    print("Sending request to RapidAPI...")
    conn.request("POST", "/clothes-virtual-tryon", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(f"Response status: {res.status}")
    print(f"Response headers: {res.getheaders()}")

    if res.status == 200:
        print("Success! Saving result...")
        with open("direct_api_result.jpg", "wb") as f:
            f.write(data)
        print("Result saved as direct_api_result.jpg")
    else:
        print(f"Error: {data.decode('utf-8')}")

if __name__ == "__main__":
    test_direct_api()

import os
import base64
import requests
import time
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from PIL import Image
import io
import uuid
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
CACHE_FOLDER = 'static/cache'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(CACHE_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['CACHE_FOLDER'] = CACHE_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.config['RATE_LIMIT_SECONDS'] = 300  # 5 minutes (300 seconds) between API calls

# API Keys
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', "1d382b59c4msh374d1f543891f32p106b59jsn93ae938cf161")
RAPIDAPI_HOST = "virtual-try-on2.p.rapidapi.com"

# Cache for API calls
LAST_API_CALL_TIME = 0

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    return base64.b64encode(image_data).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/try-on', methods=['POST'])
def try_on():
    # Check if both files are present
    if 'model_image' not in request.files or 'garment_image' not in request.files:
        flash('Both model and garment images are required')
        return redirect(request.url)

    model_file = request.files['model_image']
    garment_file = request.files['garment_image']

    # Check if files are selected
    if model_file.filename == '' or garment_file.filename == '':
        flash('No file selected')
        return redirect(request.url)

    # Check if files are allowed
    if not (allowed_file(model_file.filename) and allowed_file(garment_file.filename)):
        flash('Invalid file type. Only PNG, JPG, and JPEG are allowed')
        return redirect(request.url)

    # Save uploaded files
    model_filename = secure_filename(f"{uuid.uuid4()}_{model_file.filename}")
    garment_filename = secure_filename(f"{uuid.uuid4()}_{garment_file.filename}")

    model_path = os.path.join(app.config['UPLOAD_FOLDER'], model_filename)
    garment_path = os.path.join(app.config['UPLOAD_FOLDER'], garment_filename)

    model_file.save(model_path)
    garment_file.save(garment_path)

    # Get category from form (not used by RapidAPI but kept for future use)
    category = request.form.get('category', 'Upper body')

    try:
        # Call the RapidAPI Virtual Try-On API
        print(f"Calling API with model_path={model_path}, garment_path={garment_path}")
        result_path = call_rapidapi_tryon(model_path, garment_path, category)

        # Verify the result file exists and has content
        if not os.path.exists(result_path) or os.path.getsize(result_path) == 0:
            raise Exception("API returned an empty or invalid result")

        print(f"API call successful, result saved to {result_path}")

        # Return the result page
        return render_template('result.html',
                              original_model=model_path.replace('\\', '/'),
                              original_garment=garment_path.replace('\\', '/'),
                              result_image=result_path.replace('\\', '/'))

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in try-on route: {str(e)}")
        print(error_details)
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

def generate_cache_key(model_path, garment_path, category):
    """Generate a unique cache key based on input parameters"""
    # Read image data
    with open(model_path, 'rb') as f:
        model_data = f.read()
    with open(garment_path, 'rb') as f:
        garment_data = f.read()

    # Create a hash of the combined data
    combined = model_data + garment_data + category.encode('utf-8')
    return hashlib.md5(combined).hexdigest()

def check_cache(cache_key):
    """Check if a result exists in the cache"""
    cache_file = os.path.join(app.config['CACHE_FOLDER'], f"{cache_key}.jpg")
    if os.path.exists(cache_file):
        return cache_file
    return None

def save_to_cache(cache_key, image_data):
    """Save result to cache"""
    cache_file = os.path.join(app.config['CACHE_FOLDER'], f"{cache_key}.jpg")
    with open(cache_file, 'wb') as f:
        f.write(image_data)
    return cache_file

def call_rapidapi_tryon(model_path, garment_path, category=None):
    """Call the RapidAPI Virtual Try-On API with caching"""
    import http.client

    # Generate a cache key for this request
    cache_key = generate_cache_key(model_path, garment_path, str(category))

    # Check if result is in cache
    cached_result = check_cache(cache_key)
    if cached_result:
        print("Using cached result")
        # Copy the cached result to the results folder for consistency
        result_filename = f"result_{uuid.uuid4()}.jpg"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        with open(cached_result, 'rb') as src, open(result_path, 'wb') as dst:
            dst.write(src.read())
        return result_path

    # Read the image files
    with open(model_path, 'rb') as f:
        model_image_data = f.read()

    with open(garment_path, 'rb') as f:
        garment_image_data = f.read()

    # Method 1: Using requests library with multipart/form-data
    import requests

    url = "https://virtual-try-on2.p.rapidapi.com/clothes-virtual-tryon"

    files = {
        'personImage': ('person.jpg', model_image_data, 'image/jpeg'),
        'clothImage': ('garment.jpg', garment_image_data, 'image/jpeg')
    }

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': RAPIDAPI_HOST
    }

    try:
        response = requests.post(url, files=files, headers=headers)

        if response.status_code != 200:
            # If the first method fails, try the alternative method
            print(f"Method 1 failed with status code {response.status_code}. Trying Method 2...")
            return call_rapidapi_tryon_alt(model_path, garment_path)

        # Check if the response is JSON
        content_type = response.headers.get('Content-Type', '')
        print(f"Response content type: {content_type}")
        print(f"Response content (first 200 chars): {response.text[:200]}")

        try:
            # Try to parse as JSON
            json_response = response.json()
            print(f"JSON response: {json_response}")

            # Check if the JSON contains a URL to the result image
            if json_response.get('success') and 'response' in json_response and 'ouput_path_img' in json_response['response']:
                # Get the image URL from the JSON response
                image_url = json_response['response']['ouput_path_img']
                print(f"Image URL from API: {image_url}")

                # Download the image from the URL
                img_response = requests.get(image_url)
                if img_response.status_code != 200:
                    print(f"Failed to download image from URL: {img_response.status_code}")
                    return call_rapidapi_tryon_alt(model_path, garment_path)

                # Save the result image
                result_filename = f"result_{uuid.uuid4()}.jpg"
                result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

                # Save the image content
                with open(result_path, 'wb') as f:
                    f.write(img_response.content)

                # Save to cache
                save_to_cache(cache_key, img_response.content)

                return result_path
            else:
                print("JSON response does not contain expected image URL")
                return call_rapidapi_tryon_alt(model_path, garment_path)
        except ValueError:
            # If not JSON, check if it's an image directly
            if 'image' in content_type:
                # Save the result image
                result_filename = f"result_{uuid.uuid4()}.jpg"
                result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

                # Save the response content
                with open(result_path, 'wb') as f:
                    f.write(response.content)

                # Save to cache
                save_to_cache(cache_key, response.content)

                return result_path
            else:
                print("Response is neither JSON nor image")
                return call_rapidapi_tryon_alt(model_path, garment_path)

        return result_path
    except Exception as e:
        print(f"Method 1 failed with error: {str(e)}. Trying Method 2...")
        return call_rapidapi_tryon_alt(model_path, garment_path)

def call_rapidapi_tryon_alt(model_path, garment_path):
    """Alternative method to call the RapidAPI Virtual Try-On API using http.client"""
    import http.client

    # Read the image files
    with open(model_path, 'rb') as f:
        model_image_data = f.read()

    with open(garment_path, 'rb') as f:
        garment_image_data = f.read()

    try:
        conn = http.client.HTTPSConnection("virtual-try-on2.p.rapidapi.com")

        # Use the exact payload format from the example
        boundary = "---011000010111000001101001"

        payload = f"-----011000010111000001101001\r\n"
        payload += f"Content-Disposition: form-data; name=\"personImage\"\r\n\r\n"
        payload += f"1.jpg\r\n"
        payload += f"-----011000010111000001101001\r\n"
        payload += f"Content-Disposition: form-data; name=\"clothImage\"\r\n\r\n"
        payload += f"2.jpg\r\n"
        payload += f"-----011000010111000001101001--\r\n\r\n"

        headers = {
            'x-rapidapi-key': RAPIDAPI_KEY,
            'x-rapidapi-host': RAPIDAPI_HOST,
            'Content-Type': f"multipart/form-data; boundary={boundary}"
        }

        conn.request("POST", "/clothes-virtual-tryon", payload, headers)

        res = conn.getresponse()
        data = res.read()

        if res.status != 200:
            raise Exception(f"API request failed with status code {res.status}: {data.decode('utf-8')}")

        # Try to parse the response as JSON
        try:
            json_response = json.loads(data.decode('utf-8'))
            print(f"JSON response from alt method: {json_response}")

            # Check if the JSON contains a URL to the result image
            if json_response.get('success') and 'response' in json_response and 'ouput_path_img' in json_response['response']:
                # Get the image URL from the JSON response
                image_url = json_response['response']['ouput_path_img']
                print(f"Image URL from API (alt method): {image_url}")

                # Download the image from the URL
                img_response = requests.get(image_url)
                if img_response.status_code != 200:
                    raise Exception(f"Failed to download image from URL: {img_response.status_code}")

                # Save the result image
                result_filename = f"result_{uuid.uuid4()}.jpg"
                result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

                # Save the image content
                with open(result_path, 'wb') as f:
                    f.write(img_response.content)

                # Generate a cache key for this request
                cache_key = generate_cache_key(model_path, garment_path, "alt")

                # Save to cache
                save_to_cache(cache_key, img_response.content)

                return result_path
            else:
                raise Exception("JSON response does not contain expected image URL")
        except json.JSONDecodeError:
            # If not JSON, assume it's the image directly
            print("Response is not JSON, assuming it's the image directly")

            # Save the result image
            result_filename = f"result_{uuid.uuid4()}.jpg"
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)

            # Save the response content
            with open(result_path, 'wb') as f:
                f.write(data)

            # Generate a cache key for this request
            cache_key = generate_cache_key(model_path, garment_path, "alt")

            # Save to cache
            save_to_cache(cache_key, data)

        return result_path
    except Exception as e:
        raise Exception(f"Failed to process API request (both methods): {str(e)}")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

if __name__ == '__main__':
    app.run(debug=True)

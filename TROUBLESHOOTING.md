# Troubleshooting Guide for Virtual Try-On System

This guide will help you troubleshoot common issues with the Virtual Try-On System.

## API Key Issues

### API Key Not Set

**Symptom**: Error message "Segmind API key is not set. Please set it in the .env file."

**Solution**:
1. Make sure you have created a `.env` file in the project root directory
2. Add your API key to the file: `SEGMIND_API_KEY=your_api_key_here`
3. Restart the application

### Invalid API Key

**Symptom**: Error message "API request failed with status code 401"

**Solution**:
1. Check that your API key is correct
2. Make sure you have copied the entire key without any extra spaces
3. Verify that your account is active and has credits

## Image Processing Issues

### Incorrect Padding Error

**Symptom**: Error message containing "Incorrect padding" when processing images

**Solution**:
1. We've updated the code to handle this issue automatically
2. Make sure you're using the latest version of the code
3. If the issue persists, try using the `debug_api.py` script to diagnose the problem:
   ```
   python debug_api.py --model path/to/model/image.jpg --garment path/to/garment/image.jpg
   ```

### Image Format Issues

**Symptom**: Error when uploading or processing images

**Solution**:
1. Make sure your images are in JPG, JPEG, or PNG format
2. Check that the images are not corrupted
3. Try using different images to see if the issue persists

## API Response Issues

### Timeout or Slow Response

**Symptom**: The application seems to hang or takes a very long time to process

**Solution**:
1. The API processing can take 10-30 seconds depending on server load
2. Make sure your internet connection is stable
3. Try reducing the `num_inference_steps` parameter in the API call (in `app.py`)

### Error 429: Too Many Requests

**Symptom**: Error message "API request failed with status code 429: 1 per 5 minute" or "API rate limit exceeded"

**Solution**:
1. The Segmind API has a rate limit of 1 request per 5 minutes (300 seconds)
2. The application now implements caching to avoid hitting this limit
3. If you see this error, wait for the specified time before trying again
4. For testing purposes, you can use the `--force` flag with the test scripts:
   ```
   python test_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg --force
   ```
5. The application will use cached results when possible to avoid hitting the rate limit

## Application Issues

### Application Won't Start

**Symptom**: Error when trying to run the application

**Solution**:
1. Make sure you have installed all dependencies: `pip install -r requirements.txt`
2. Check that you're using Python 3.7 or higher
3. Verify that all required directories exist (they should be created automatically)

### Images Not Displaying

**Symptom**: Images are not visible in the application

**Solution**:
1. Check that the `static/uploads` and `static/results` directories exist and are writable
2. Verify that the image paths in the templates are correct
3. Clear your browser cache and reload the page

## Testing the API

If you're having issues with the API, you can use the included test scripts to diagnose the problem:

1. Test the API with sample images:
   ```
   python test_api.py --model path/to/model/image.jpg --garment path/to/garment/image.jpg
   ```

2. Debug the API response:
   ```
   python debug_api.py --model path/to/model/image.jpg --garment path/to/garment/image.jpg
   ```

## Getting Help

If you continue to experience issues:

1. Check the API provider's documentation and status page
2. Look for error messages in the console output
3. Try with different images and garment categories
4. Contact the API provider's support team if you believe the issue is with their service

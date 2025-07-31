# Testing Guide for Virtual Try-On System

This guide will help you test the Virtual Try-On System using the provided sample images and test scripts.

## Using Sample Images

We've created sample images in the `static/img` directory that you can use for testing:

- `sample_person.jpg`: A sample person image
- `sample_shirt.jpg`: A sample garment image

These are simple placeholder images. For better results, you should use real photos of people and garments.

## Testing the API

### 1. Basic API Test

To test if your API key is working and the API is responding correctly:

```
python test_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg
```

This will:
- Check if the rate limit has expired (1 request per 5 minutes)
- Send a request to the Segmind API if the rate limit allows
- Save the result as `api_test_result.jpg` in the current directory
- Display success or error messages

**Note about Rate Limits**: The Segmind API has a rate limit of 1 request per 5 minutes. If you need to bypass this limit for testing, use the `--force` flag:

```
python test_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg --force
```

Be aware that forcing requests may still result in 429 errors from the API.

### 2. Debugging the API

If you're having issues with the API, you can use the debugging script for more detailed information:

```
python debug_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg
```

This will:
- Check if the rate limit has expired (1 request per 5 minutes)
- Send a request to the Segmind API if the rate limit allows
- Display detailed information about the response
- Save the result as `debug_api_result.jpg` in the current directory

You can also use the `--force` flag to bypass the rate limit check:

```
python debug_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg --force
```

### 3. Specifying Garment Category

You can specify the garment category using the `--category` parameter:

```
python test_api.py --model static/img/sample_person.jpg --garment static/img/sample_shirt.jpg --category "Upper body"
```

Valid categories are:
- "Upper body" (for shirts, t-shirts, jackets, etc.)
- "Lower body" (for pants, skirts, shorts, etc.)
- "Dress" (for full dresses)

## Using Your Own Images

For better results, you should use your own images:

1. **Person Image Requirements**:
   - Front-facing, full-body photo
   - Neutral background
   - Good lighting
   - Clear visibility of the person

2. **Garment Image Requirements**:
   - White or transparent background
   - Front view of the garment
   - Good lighting
   - Clear visibility of the garment details

Example:
```
python test_api.py --model path/to/your/person.jpg --garment path/to/your/garment.jpg
```

## Running the Full Application

Once you've confirmed that the API is working, you can run the full application:

```
python run.py
```

Then open your web browser and go to:
```
http://127.0.0.1:5000/
```

## Troubleshooting

If you encounter issues:

1. Check that your API key is correctly set in the `.env` file
2. Verify that the sample images exist in the `static/img` directory
3. Make sure you have installed all dependencies: `pip install -r requirements.txt`
4. Refer to the `TROUBLESHOOTING.md` file for common issues and solutions

## Next Steps

After successful testing:

1. Replace the sample images with real photos
2. Customize the application to suit your needs
3. Deploy the application to a web server (optional)
4. Share your virtual try-on experience with others

# Virtual Try-On System

A Flask-based web application that allows users to virtually try on clothing items using AI technology.

## Features

- Upload your photo and a garment image
- AI-powered virtual try-on using the Segmind Try-On Diffusion API
- Support for different garment categories (upper body, lower body, dress)
- Responsive design for desktop and mobile devices
- Image preview before submission
- Download and share try-on results

## Prerequisites

- Python 3.7 or higher
- Flask
- Requests
- Pillow
- Python-dotenv

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/virtual-try-on.git
   cd virtual-try-on
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root directory and add your API key:
   ```
   SEGMIND_API_KEY=your_segmind_api_key_here
   ```

## Getting an API Key

### Segmind API Key

1. Go to [Segmind](https://www.segmind.com/)
2. Sign up for an account
3. Navigate to your account dashboard
4. Go to API Keys section
5. Generate a new API key
6. Copy the API key and add it to your `.env` file

### Alternative: FASHN API Key

If you prefer to use the FASHN API:

1. Go to [FASHN.AI](https://fashn.ai/)
2. Sign up for an account
3. Navigate to the API section
4. Generate a new API key (starts at $10)
5. Copy the API key and add it to your `.env` file as `FASHN_API_KEY`
6. Modify the `app.py` file to use the FASHN API instead of Segmind

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

3. Upload your photo and a garment image, select the garment category, and click "Try On Now"

4. View, download, or share the result

## Project Structure

```
virtual-try-on/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (API keys)
├── .env.example            # Example environment file
├── README.md               # Project documentation
├── static/                 # Static files
│   ├── css/                # CSS stylesheets
│   │   └── style.css       # Main stylesheet
│   ├── js/                 # JavaScript files
│   │   └── main.js         # Main JavaScript file
│   └── img/                # Images
│       ├── person-placeholder.jpg
│       ├── garment-placeholder.jpg
│       └── how-it-works.jpg
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── result.html         # Results page
│   ├── about.html          # About page
│   └── how_it_works.html   # How it works page
├── uploads/                # Uploaded images (created at runtime)
└── results/                # Generated results (created at runtime)
```

## Screenshots
<img width="1920" height="1080" alt="Screenshot 2025-07-31 113341" src="https://github.com/user-attachments/assets/545b2e3f-4dd0-41ee-b682-a19910ca58e3" />


## Limitations

- The quality of the try-on result depends on the quality of the input images
- Best results are achieved with front-facing, full-body photos against a neutral background
- Garment images should have a white or transparent background
- Complex patterns or unusual garment shapes may not render perfectly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Segmind](https://www.segmind.com/) for providing the Try-On Diffusion API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the UI components

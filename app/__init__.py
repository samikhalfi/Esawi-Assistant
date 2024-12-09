import os
from flask import Flask
import google.generativeai as genai

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables for API keys (Gemini API, etc.)
app.config['GENAI_API_KEY'] = os.getenv('GENAI_API_KEY', 'your_default_api_key_here')

# Initialize the Gemini API client
def init_genai():
    api_key = app.config['GENAI_API_KEY']
    if api_key:
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully.")
    else:
        print("Gemini API key not found. Please set it in environment variables.")

# Call the initialization function
init_genai()

# You can also import your views, models, and other components here
from . import routes

# Flask app setup
if __name__ == "__main__":
    app.run(debug=True)

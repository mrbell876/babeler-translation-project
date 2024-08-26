from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from textprocessor import translate_text
from imageprocessor import extract_and_translate_text_from_file
from videoprocessor import extract_and_translate_text_from_video
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    query = data.get('query')
    source_lang = data.get('source_lang')
    
    
    translation = translate_text(query, source_lang)
    
    return jsonify({'translation': translation})

@app.route('/translate_image', methods=['POST'])
def translate_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    source_lang = request.form.get('source_lang')  # Get source language from the form data
    
    result = extract_and_translate_text_from_file(file, source_lang)
    
    return jsonify(result)

@app.route('/translate_video', methods=['POST'])
def translate_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    result = extract_and_translate_text_from_video(file)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

import cv2
import pytesseract
from PIL import Image
import numpy as np
from PyPDF2 import PdfReader
import re
from textprocessor import translate_text
from flask import Flask, request

# Set up Tesseract OCR configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert to grayscale (if not already in grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply denoising
    denoised_image = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    # Improve contrast using CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrasted_image = clahe.apply(denoised_image)

    # Apply adaptive thresholding to get a binary image
    thresh = cv2.adaptiveThreshold(contrasted_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Resize the image to enhance OCR accuracy
    resized = cv2.resize(thresh, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    return resized

def clean_text(text):
    # Remove excess spaces and correct common OCR errors
    text = re.sub(r'\s+', ' ', text)  # Collapse multiple spaces into one
    text = re.sub(r'\s([?.!",])', r'\1', text)  # Remove spaces before punctuation
    return text.strip()

def extract_and_translate_text_from_file(file, source_lang):
    file_extension = file.filename.rsplit('.', 1)[-1].lower()
    
    if file_extension in ['png', 'jpg', 'jpeg', 'gif']:
        image = Image.open(file.stream)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        preprocessed_image = preprocess_image(image)
        
        if source_lang.lower() == 'english':
            tess_config = '--oem 3 --psm 3 -l eng'
        elif source_lang.lower() == 'spanish':
            tess_config = '--oem 3 --psm 3 -l spa'
        else:
            return {"error": "Unsupported source language selected."}
        
        text = pytesseract.image_to_string(preprocessed_image, config=tess_config)
        text = clean_text(text)  # Clean up the extracted text
    
    elif file_extension == 'pdf':
        pdf_reader = PdfReader(file.stream)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        text = clean_text(text)  # Clean up the extracted text
    
    else:
        return {"error": "Unsupported file type. Please upload an image or PDF."}
    
    translation = translate_text(text, source_lang)
    
    return {'translation': translation, 'extracted_text': text}

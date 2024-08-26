import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
import openai
import os

# Initialize the sentence transformer model
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

def fetch_closest_translation(query, source_lang):
    query_embedding = sentence_model.encode(query)
    
    conn = sqlite3.connect('translations.db')
    c = conn.cursor()
    if source_lang== 'english':
        language_column = 'english'
        embedding_column = 'english_embedding'
    elif source_lang == 'spanish':
        language_column = 'spanish'
        embedding_column = 'spanish_embedding'
    else:
        raise ValueError("Unsupported source language")
    
    c.execute(f"SELECT id, {language_column}, {embedding_column} FROM translations")
    translations = c.fetchall()
    
    distances = []
    for translation in translations:
        translation_embedding = np.frombuffer(translation[2], dtype=np.float32)
        distance = np.linalg.norm(query_embedding - translation_embedding)
        distances.append((distance, translation[1]))
    
    closest_translation = min(distances, key=lambda x: x[0])[1]
    
    conn.close()
    return closest_translation

def generate_gpt3_translation(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can use other models like gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100  # Adjust the token limit based on your needs
    )
    return response.choices[0].message['content'].strip()

def translate_text(query, source_lang):
    if source_lang == 'english':
        target_lang = 'spanish'
    else:
        target_lang = 'english'
    
    # Fetch the closest translation
    closest_translation = fetch_closest_translation(query, source_lang)
    
    # Use GPT-3 to generate the translation
    prompt = (f"Given the closest translation from the vector database and use if correct if not use for context: '{closest_translation}', "
              f"translate the following {source_lang} text to {target_lang}: '{query}' and if text is incomplete or has errors give the best possible translation and return the original input text")
    translation = generate_gpt3_translation(prompt)
    
    return translation

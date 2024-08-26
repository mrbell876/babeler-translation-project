import sqlite3
from sentence_transformers import SentenceTransformer
import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the CSV file
csv_file_path = r'C:\Users\javid\babeler\UN_parallel_corpus_20000.csv'

try:
    # Load the UN 2000 corpus
    logging.info(f'Loading data from {csv_file_path}')
    data = pd.read_csv(csv_file_path)
except FileNotFoundError:
    logging.error(f'File not found: {csv_file_path}')
    raise
except pd.errors.EmptyDataError:
    logging.error('No data found in the CSV file')
    raise
except Exception as e:
    logging.error(f'Error loading data: {e}')
    raise

# Initialize the sentence transformer model
logging.info('Initializing sentence transformer model')
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create the database
try:
    logging.info('Connecting to the database')
    conn = sqlite3.connect('translations.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY, 
                    english TEXT, 
                    spanish TEXT, 
                    english_embedding BLOB, 
                    spanish_embedding BLOB)''')
except sqlite3.Error as e:
    logging.error(f'Error connecting to database: {e}')
    raise

# Populate the database
try:
    logging.info('Populating the database')
    for idx, row in data.iterrows():
        english_embedding = model.encode(row['English']).tobytes()
        spanish_embedding = model.encode(row['Spanish']).tobytes()
        c.execute("INSERT INTO translations (english, spanish, english_embedding, spanish_embedding) VALUES (?, ?, ?, ?)",
                  (row['English'], row['Spanish'], english_embedding, spanish_embedding))
    conn.commit()
except Exception as e:
    logging.error(f'Error populating database: {e}')
finally:
    conn.close()
    logging.info('Database connection closed')

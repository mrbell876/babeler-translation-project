# babeler-translation-project
combing rag and ocr to complete translation tasks in english and spanish
Technical documentation

Overview of the Application and Its Architecture
The application integrates advanced techniques to deliver accurate and contextually relevant translations, employing Retrieval-Augmented Generation (RAG) and Optical Character Recognition (OCR). It processes text, images, and videos to provide comprehensive translation services. It was deployed using flask and its api and for the flexibility of being able to be deployed on multiple hosting services or platforms without needing much adjustments to the source code 
r

Architecture:
Retrieval-Augmented Generation (RAG): Enhances language models by incorporating external data, reducing hallucinations and improving response accuracy.
Optical Character Recognition (OCR): Extracts text from images and PDFs for subsequent translation using the RAG model.
Multimodal Input Handling: Adapts techniques for handling text, images, and videos to ensure accurate translations.

Retrieval-Augmented Generation (RAG)
Retrieval-Augmented Generation (RAG) advances language models by integrating external information into the generation process, addressing limitations of pre-trained data alone. This approach reduces hallucinations and provides more accurate and relevant responses by incorporating up-to-date information (Finardi et al., 2024).


Data Cleaning and Preparation
Data preparation for RAG involves several key steps:
Loading and Sampling Data: The UN 2000 corpus, a parallel dataset with English-Spanish sentence pairs, was sampled to create a balanced dataset for training and evaluation.
Tokenization and Vector Embeddings: Text data were tokenized using the DPRContextEncoderTokenizer for English and the BartTokenizer for Spanish. Vector embeddings were generated with the SentenceTransformer model, converting text into numerical format suitable for machine learning.
Database Creation: Embeddings were stored in an SQLite database for efficient retrieval during training and evaluation. The database had 1 table with 2 columns 1 for each language and 1 for the embeddings of each language. A fetch function was used to retrieve similar vectors from the database after the user input was converted to a vector or vectors.








RAG Modeling Results
Three models were evaluated:
BART Model: Due to resource constraints, this model was trained on a sampled dataset. The evaluation results are:

Metric
Score
BLEU Score
0.8136
ROUGE-1 F1 Score
0.1668
ROUGE-L F1 Score
0.1332


GPT-3.5 Turbo (Without Augmentation):
Metric
Score
ROUGE-1
0.6056
ROUGE-2
0.3855
ROUGE-L
0.5596
BLEU Score
0.2564





GPT-3.5 Turbo (With Augmentation):

Metric
Score
ROUGE-1
0.5648
ROUGE-2
0.3601
ROUGE-L
0.5228
BLEU Score
0.2459

The GPT-3.5 Turbo model was preferred for its lower resource demands, allowing it to be trained on a larger dataset and offering greater flexibility in deployment.








Optical Character Recognition (OCR)
Optical Character Recognition (OCR) is crucial for text extraction from images and PDFs. Google Tesseract was chosen for its robustness and adaptability.
Data Cleaning and Preparation
OCR data preparation involved:
Grayscale Conversion: Images were converted to grayscale to enhance text contrast and reduce computational complexity.
Rotation Correction: Images were adjusted to ensure correct text alignment and orientation.
Noise Reduction and Filtering: Techniques such as Gaussian blur and thresholding were applied to improve text clarity and remove background noise.
LSTM Architecture for OCR
Long Short-Term Memory (LSTM) networks are a type of Recurrent Neural Network (RNN) designed to handle long-term dependencies in sequential data. LSTMs are effective for OCR tasks due to their ability to remember long-term context and recognize patterns over sequences. Key components include:
Cell State: Maintains information over long sequences.
Forget Gate: Decides which information to discard.
Input Gate: Controls the addition of new information to the cell state.
Output Gate: Determines the next hidden state based on the cell state.
LSTMs enable OCR models to learn and recognize language-specific patterns, improving text extraction accuracy.
OCR Modeling Results
Two OCR models were evaluated:
Base OCR Model:
Metric
Score
Precision
0.6263
Recall
0.9841
F1 Score
0.7654



OCR with Parameters:
Metric
Score
Precision
0.6176
Recall
1.0
F1 Score
0.7636

The base OCR model demonstrated higher recall, indicating it was more effective at identifying all relevant text, while the parameter-tuned model showed slightly better precision.



Data Description
UN 2000 Corpus
The UN 2000 corpus is a parallel dataset with aligned English-Spanish sentence pairs, extracted from United Nations proceedings. It is a valuable resource for training and evaluating translation models. For further details, refer to the paper by Koehn (2005) and the extended report.
Tesseract OCR Training Data
The Tesseract OCR training data includes English and Spanish datasets with examples of handwritten text, facilitating OCR model training.
corto-ai/handwritten-text Dataset
The corto-ai/handwritten-text dataset, from the Hugging Face datasets library, contains 10,373 images of handwritten text in English. It is used for testing OCR models and evaluating their performance on real-world handwritten text samples.






Conclusion
The successful completion of this project demonstrates the effective integration of Optical Character Recognition (OCR) and Retrieval-Augmented Generation (RAG) techniques to address critical needs in multilingual environments. Our application, designed to extract and translate text from images in both English and Spanish, achieves notable advancements in text recognition and translation accuracy.
The OCR component of the project utilized two models: a base Tesseract OCR and a tuned version with adjusted parameters. The results indicated that while both models performed well, the base OCR model offered higher precision, whereas the tuned model excelled in recall. These findings underscore the importance of balancing precision and recall based on specific application needs.
For the RAG modeling, our approach compared several translation models, including a fine-tuned BART model, GPT-3.5-turbo without augmentation, and GPT-3.5-turbo with augmented prompts. The BART model, despite resource constraints, demonstrated strong BLEU and ROUGE scores, highlighting its effectiveness in translation tasks. The GPT-3.5-turbo models provided flexibility, with the augmented model offering improved performance in translation quality compared to the non-augmented version. The choice of GPT-3.5-turbo was particularly advantageous due to its resource efficiency and scalability for larger datasets.
Overall, this project not only advances the capabilities of text extraction and translation but also supports business expansion and communication in international settings. The application promises to streamline document digitization and translation processes, making it a valuable tool for facilitating cross-language communication and supporting global business operations













import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
import numpy as np
import os
from textprocessor import translate_text

def preprocess_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    
    return audio

def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    
    audio = preprocess_audio(audio_path)
    audio.export(audio_path, format="wav")
    
    return audio_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    
    with audio_file as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio, language="en-ES")
    except sr.UnknownValueError:
        text = ""
    
    return text

def extract_and_translate_text_from_video(file):
    video_path = "temp_video.mp4"
    file.save(video_path)
    
    audio_path = extract_audio_from_video(video_path)
    text = transcribe_audio(audio_path)
    
    if any(char in 'áéíóúüñÁÉÍÓÚÜÑ' for char in text):
        source_lang = 'spanish'
    else:
        source_lang = 'english'
    
    translation = translate_text(text, source_lang)
    
    os.remove(video_path)
    os.remove(audio_path)
    
    return {'translation': translation, 'extracted_text': text}

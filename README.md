## BookAI - Listen to Books with Enhanced Audio Processing

## Overview

BookAI is a Streamlit-based web application that enables users to upload PDF books and convert them into audio files. With options for file management, language selection, and flexible processing methods, BookAI makes it easy to listen to books in various formats and languages.

## Features

# Upload Books

Supports PDF files up to 200MB.

Automatically saves uploaded books in structured directories.

Flexible Processing Options

Convert books to audio by pages or process the entire book in one go.

Support for chunk-based processing for better memory management.

# Multiple TTS Engines

Google Cloud TTS: Premium text-to-speech service.

gTTS (Free Online TTS): Free online option.

pyttsx3 (Offline TTS): No internet required.

# Multi-Language Support

English, Spanish, French, German, and Hindi. (right now only english)

# Audio File Management

Each book is stored in a dedicated folder.

Audio files are named based on pages or chunks for easy navigation.

# Interactive Dashboard

Real-time progress tracking during processing.

Playback and download options for generated audio files.

# Prerequisites
Before running the project, ensure you have the following installed:

Python 3.8+

Required Python libraries (install with pip):

pip install streamlit google-cloud-texttospeech gtts pyttsx3 pymupdf 

# How to Run
Clone the repository or download the code.
Navigate to the project folder.
Run the application using Streamlit:
streamlit run data.py
Upload a book (PDF format only), select a TTS engine and language, and process the book.

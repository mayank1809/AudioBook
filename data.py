import os
import streamlit as st
from google.cloud import texttospeech
from gtts import gTTS  # Free TTS
import pyttsx3  # Offline TTS
import fitz  # PyMuPDF


# Extract text from PDF (optionally by chapters or pages)
def extract_text_from_pdf(file_path, option="pages", page_range=None):
    try:
        doc = fitz.open(file_path)
        if option == "pages":
            # Extract by page range
            text = ""
            for page_num in page_range:
                page = doc.load_page(page_num)
                text += page.get_text()
            return text
        elif option == "whole":  # For entire book
            return "\n".join(page.get_text() for page in doc)
        elif option == "chapters":  # Placeholder if chapters are structured
            st.warning("Chapter-based extraction is not yet implemented!")
            return ""
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""


# Google Cloud TTS
def google_tts(text, lang_code, output_file):
    try:
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
    except Exception as e:
        st.error(f"Error in Google Cloud TTS: {e}")


# gTTS (Free Online TTS)
def gtts_tts(text, lang_code, output_file):
    try:
        tts = gTTS(text=text, lang=lang_code)
        tts.save(output_file)
    except Exception as e:
        st.error(f"Error in gTTS: {e}")


# pyttsx3 (Offline TTS)
def pyttsx3_tts(text, output_file):
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_file)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error in pyttsx3 TTS: {e}")


# Process the book based on user options
def process_book(file_path, tts_option, lang_code, output_dir, option="pages"):
    doc = fitz.open(file_path)
    num_pages = len(doc)
    st.text(f"Total Pages in Book: {num_pages}")
    os.makedirs(output_dir, exist_ok=True)

    audio_files = []
    if option == "pages":
        for page_num in range(num_pages):
            text = extract_text_from_pdf(file_path, option="pages", page_range=[page_num])
            output_file = os.path.join(output_dir, f"Page_{page_num + 1}.mp3")
            if tts_option == "Google Cloud TTS":
                google_tts(text, lang_code, output_file)
            elif tts_option == "pyttsx3 (Offline TTS)":
                pyttsx3_tts(text, output_file)
            elif tts_option == "gTTS (Free Online TTS)":
                gtts_tts(text, lang_code, output_file)
            audio_files.append(output_file)
            st.text(f"Processed Page {page_num + 1}/{num_pages}")
    elif option == "whole":
        text = extract_text_from_pdf(file_path, option="whole")
        output_file = os.path.join(output_dir, f"Whole_Book.mp3")
        if tts_option == "Google Cloud TTS":
            google_tts(text, lang_code, output_file)
        elif tts_option == "pyttsx3 (Offline TTS)":
            pyttsx3_tts(text, output_file)
        elif tts_option == "gTTS (Free Online TTS)":
            gtts_tts(text, lang_code, output_file)
        audio_files.append(output_file)
    return audio_files


# Streamlit App
st.title("📚 BookAI - Enhanced File Management and Audio Processing")
uploaded_file = st.file_uploader("Upload a book (PDF format only):", type=["pdf"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    file_path = os.path.join("uploaded_books", file_name)

    # Save the uploaded file
    os.makedirs("uploaded_books", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File '{file_name}' uploaded successfully!")

    # TTS Engine Selection
    tts_options = ["Google Cloud TTS", "pyttsx3 (Offline TTS)", "gTTS (Free Online TTS)"]
    tts_option = st.radio("Choose the Text-to-Speech engine:", tts_options)

    # Language Selection
    language_options = {"English": "en", "Spanish": "es", "French": "fr", "German": "de", "Hindi": "hi"}
    lang_code = st.selectbox("Select the language for narration:", list(language_options.keys()))
    lang_code = language_options[lang_code]

    # File Processing Option
    process_options = ["pages", "whole"]
    process_option = st.radio("Process the book by:", ["Pages", "Whole Book"])
    process_option = process_options[0] if process_option == "Pages" else process_options[1]

    if st.button("Run"):
        with st.spinner("Processing your book..."):
            output_dir = os.path.join("uploaded_books", os.path.splitext(file_name)[0])
            audio_files = process_book(file_path, tts_option, lang_code, output_dir, process_option)
            st.success("Audio files generated successfully!")

            # Display and Download Audio Files
            for audio_file in audio_files:
                with open(audio_file, "rb") as audio:
                    audio_bytes = audio.read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(f"Download {os.path.basename(audio_file)}", data=audio_bytes, file_name=os.path.basename(audio_file), mime="audio/mp3")

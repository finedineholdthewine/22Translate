import streamlit as st
from deep_translator import GoogleTranslator
import pykakasi
from gtts import gTTS
from io import BytesIO

# Set up romaji converter
kakasi = pykakasi.kakasi()

# Page settings
st.set_page_config(page_title="Japanese-English Translator", layout="centered")
st.title("🈺 Japanese ⇄ English Translator")

# Translation direction
direction = st.radio("Choose translation direction:", ("Japanese → English", "English → Japanese"))

# Text input
text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        src_lang = "ja" if direction == "Japanese → English" else "en"
        target_lang = "en" if src_lang == "ja" else "ja"

        try:
            # Translate the text
            translated_text = GoogleTranslator(source=src_lang, target=target_lang).translate(text_input)
            st.success("Translation:")
            st.write(translated_text)

            # Show Romaji if translating to Japanese
            if target_lang == "ja":
                result = kakasi.convert(translated_text)
                romaji = " ".join([item['hepburn'] for item in result])
                st.info("Pronunciation (Romaji):")
                st.write(romaji)

# Text-to-speech (Streamlit Cloud safe with error handling)
    try:
    tts_lang = 'ja' if target_lang == 'ja' else 'en'
    tts = gTTS(text=translated_text, lang=tts_lang)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    st.audio(mp3_fp, format='audio/mp3')
except Exception as e:
    st.warning("Sorry! I couldn’t pronounce that sentence. Try a shorter or simpler one.")

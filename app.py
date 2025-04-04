import streamlit as st
from deep_translator import GoogleTranslator
import pykakasi
from gtts import gTTS
from io import BytesIO

# Setup for Romaji converter
kakasi = pykakasi.kakasi()

# Page setup
st.set_page_config(page_title="Japanese-English Translator", layout="centered")
st.title("🈺 Japanese ⇄ English Translator")

# Language direction
direction = st.radio("Choose translation direction:", ("Japanese → English", "English → Japanese"))

# Text input box
text_input = st.text_area("Enter text to translate:", height=150)

# When Translate button is clicked
if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Set source and target languages
        src_lang = "ja" if direction == "Japanese → English" else "en"
        target_lang = "en" if src_lang == "ja" else "ja"

        try:
            # Translate
            translated_text = GoogleTranslator(source=src_lang, target=target_lang).translate(text_input)
            st.success("Translation:")
            st.write(translated_text)

            # Show Romaji if output is Japanese
            if target_lang == "ja":
                result = kakasi.convert(translated_text)
                romaji = " ".join([item['hepburn'] for item in result])
                st.info("Pronunciation (Romaji):")
                st.write(romaji)

            # Speak the result (audio output)
            try:
                tts_lang = 'ja' if target_lang == 'ja' else 'en'
                tts = gTTS(text=translated_text, lang=tts_lang)
                mp3_fp = BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                st.audio(mp3_fp, format='audio/mp3')
            except Exception as audio_error:
                st.warning("Sorry! I couldn’t pronounce that sentence.")

        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")

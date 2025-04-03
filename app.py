import streamlit as st
from deep_translator import GoogleTranslator
import pykakasi
from gtts import gTTS
import tempfile

# Set up pronunciation tool
kakasi = pykakasi.kakasi()

# Page setup
st.set_page_config(page_title="Japanese-English Translator", layout="centered")
st.title("🈺 Japanese ⇄ English Translator")

# Direction selection
direction = st.radio("Choose translation direction:", ("Japanese → English", "English → Japanese"))

# User input
text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        # Figure out the languages
        src_lang = "ja" if direction == "Japanese → English" else "en"
        target_lang = "en" if src_lang == "ja" else "ja"

        try:
            # Translate it
            translated_text = GoogleTranslator(source=src_lang, target=target_lang).translate(text_input)
            st.success("Translation:")
            st.write(translated_text)

            # If it's Japanese output, show romaji too
            if target_lang == "ja":
                result = kakasi.convert(translated_text)
                romaji = " ".join([item['hepburn'] for item in result])
                st.info("Pronunciation (Romaji):")
                st.write(romaji)

            # Text-to-speech part
            tts_lang = 'ja' if target_lang == 'ja' else 'en'
            tts = gTTS(text=translated_text, lang=tts_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')

        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")

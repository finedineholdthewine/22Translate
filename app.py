import streamlit as st
from deep_translator import GoogleTranslator
import pykakasi
from gtts import gTTS
import tempfile
import os

# Setup
kakasi = pykakasi.kakasi()
st.set_page_config(page_title="Japanese-English Translator", layout="centered")
st.title("🈺 Japanese ⇄ English Translator")

direction = st.radio("Choose translation direction:", ("Japanese → English", "English → Japanese"))
text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate"):
    if text_input.strip() == "":
        st.warning("Please enter some text.")
    else:
        src_lang = "ja" if direction == "Japanese → English" else "en"
        target_lang = "en" if src_lang == "ja" else "ja"

        try:
            # Translation
            translated_text = GoogleTranslator(source=src_lang, target=target_lang).translate(text_input)
            st.success("Translation:")
            st.write(translated_text)

            # Romaji if Japanese output
            if target_lang == "ja":
                result = kakasi.convert(translated_text)
                romaji = " ".join([item['hepburn'] for item in result])
                st.info("Pronunciation (Romaji):")
                st.write(romaji)

            # Text-to-Speech
            tts = gTTS(text=translated_text, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                st.audio(fp.name, format='audio/mp3')
                os.unlink(fp.name)  # Cleanup after playback

        except Exception as e:
            st.error(f"Translation failed: {e}")

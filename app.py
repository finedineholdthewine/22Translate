import streamlit as st
from deep_translator import GoogleTranslator

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
            translated_text = GoogleTranslator(source=src_lang, target=target_lang).translate(text_input)
            st.success("Translation:")
            st.write(translated_text)
        except Exception as e:
            st.error(f"Translation failed: {e}")

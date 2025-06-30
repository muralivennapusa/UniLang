import streamlit as st
import pyttsx3

def text_to_speech(text, output_file):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_file)
    engine.runAndWait()

text = '''
    கடல் என்பது காற்று காயும் காயும்
   இடல் என்பது மண் காயும் காயும்
'''
output_audio_file = "test.mp3"
print(output_audio_file)
text_to_speech(text, output_audio_file)

st.audio(output_audio_file, format="audio/mpeg", loop=True)

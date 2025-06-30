import streamlit as st
from openai import OpenAI

import pyttsx3

import json
import datetime


def Prompt_History():
    file_path="history.json"
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data:
                if len(entry["message"])<=1:
                    continue
                st.write("Timestamp:",entry["timestamp"])
                
                st.markdown("## Prompt:\n")
                st.code(entry["message"]+"\n",language="text")
                st.markdown("## Response:\n")
                st.code(entry["Response"]+"\n",language="text")
                st.markdown("---")
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid data found.")

def Multiligual_NLP():
    def write_to_json(message,response):
        file_path="history.json"
        timestamp = datetime.datetime.now().isoformat()
        new_entry = {"timestamp": timestamp, "message": message,"Response":response}
        
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                if not isinstance(data, list):  # Ensure data is a list
                    data = []
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(new_entry)
        
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


    base_url = "https://api.aimlapi.com/v1"
    api_key = "REDACTED"
    #apikey=open("apikey.txt",'r').read()

    api = OpenAI(api_key=api_key, base_url=base_url)

    st.title("Multilingual model")
    st.markdown("Enter your message below and get an AI-generated response.")

    user_prompt = st.text_input("User:","")
    if len(user_prompt)<5:
        st.warning("Message should be at least 5 characters long.")
        return

    if st.button("Send") and user_prompt:
        system_prompt = "You are a language agnostic model."
        
        completion = api.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=10,
        )
        
        response = completion.choices[0].message.content
        st.markdown("AI:")
        st.markdown(response)
        write_to_json(user_prompt,response)

        def text_to_speech(text, output_file):
            engine = pyttsx3.init()
            engine.save_to_file(text, output_file)
            engine.runAndWait()

        text = response
        output_audio_file = "test.mp3"
        print(output_audio_file)
        text_to_speech(text, output_audio_file)
        st.audio(output_audio_file, format="audio/mpeg", loop=False)
        
    # response='''
    #     # Quotes Collection

    # ## Gaming Quotes
    # - "Gamers don't die, they respawn."
    # - "It's now or never (but yesterday would have been better)."
    # - "Victory is just a respawn away."
    # - "Keep calm and press start."
    # - "Eat, sleep, game, repeat."

    # ## Motivational Quotes
    # - "Dream big, start small, act now."
    # - "Doubt kills more dreams than failure ever will."
    # - "Don't stop when you're tired, stop when you're done."
    # - "Failure is the first step to success."
    # - "Every accomplishment starts with the decision to try."

    # '''

page_names_to_funcs = {
    "Multilingual NLP": Multiligual_NLP,
    "Prompt History": Prompt_History,
}

demo_name = st.sidebar.selectbox("Access Points/ Navigation", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
"""app.py

Examples:
    $ streamlit run chatefficient/app_openai.py
"""
import streamlit as st
from joblib import Memory
from openai import OpenAI

LOCATION = "./cachedir"
MEMORY = Memory(LOCATION, verbose=0)
CLIENT = OpenAI()


@MEMORY.cache
def generate_response(prompt, model="gpt-3.5-turbo"):
    """Prompt GPT API for a chat completion response."""
    st.session_state["context"].append({"role": "user", "content": prompt})

    completion = CLIENT.chat.completions.create(model=model, messages=st.session_state["context"])
    response = completion.choices[0].message.content
    st.session_state["context"].append({"role": "assistant", "content": response})

    return response


# Initialize session state variables
if "context" not in st.session_state:
    st.session_state["context"] = [{"role": "system", "content": "You are a helpful assistant."}]

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


# Containers
response_container = st.container()
chat_container = st.container()


with chat_container:
    if prompt := st.chat_input("Say something"):
        output = generate_response(prompt)
        st.session_state["past"].append(prompt)
        st.session_state["generated"].append(output)

if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            st.chat_message("user").write(st.session_state["past"][i])
            st.chat_message("ai").write(st.session_state["generated"][i])

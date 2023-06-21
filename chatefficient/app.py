"""app.py

Docs: ???

Examples:
    $ streamlit run chatefficient/app.py
"""
import openai
import streamlit as st
from joblib import Memory
from streamlit_chat import message

LOCATION = "./cachedir"
MEMORY = Memory(LOCATION, verbose=0)


@MEMORY.cache
def generate_response(prompt, model="gpt-3.5-turbo"):
    """Prompt GPT API for a chat completion response."""
    st.session_state["context"].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(model=model, messages=st.session_state["context"])
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
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        output = generate_response(user_input)
        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(output)


if st.session_state["generated"]:
    with response_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=f"{i}_user")
            message(st.session_state["generated"][i], key=f"{i}")

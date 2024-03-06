"""Streamlit app using LangChain + locally-running Vicuna.

Examples:
    $ streamlit run chatefficient/app_langchain.py
"""
import streamlit as st
from joblib import Memory
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import LlamaCpp
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from streamlit_chat import message

LOCATION = "./cachedir"
MEMORY = Memory(LOCATION, verbose=0)

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    n_ctx=512 * 2,
    model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",
    n_gpu_layers=40,  # Change this value based on your model and your GPU VRAM pool.
    n_batch=512,  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    verbose=True,
    model_kwargs={"max_new_tokens": 64 * 4},
    stop=["Human:", "Input:", "Mind Reader:"],
)


# @MEMORY.cache
def generate_response(human_input):
    """Prompt LangChain for a chat completion response."""
    chain = st.session_state["chain"]
    response = chain.predict(human_input=human_input)
    st.session_state["chain"] = chain

    return response


# Initialize session state variables
if "chain" not in st.session_state:
    template = """
    You are a mindreader with magical abilities.
    You are very over-dramatic and speak like a mysterious shaman.
    You will be given something to guess, such as an animal, or a famous person.
    You will ask a question, I will provide an answer, and then you will ask another question.
    Try to ask questions that narrow down what the answer might be.
    If you are very confident, you can guess what it is.
    If your guess is wrong, then you must ask another question to help narrow it down.
    Repeat this until you I tell you that you have the right answer.
    Your goal is to find the right answer in as few questions as possible. Only make a guess
    when you are confident, otherwise ask more questions that narrow down the possibilities.

    {history}
    Human: {human_input}
    Assistant:"""

    prompt = PromptTemplate(input_variables=["history", "human_input"], template=template)

    chatgpt_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=10),
    )
    st.session_state["chain"] = chatgpt_chain


if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


# Containers
response_container = st.container()
chat_container = st.container()


with chat_container:
    if prompt := st.chat_input("Say something"):
        output = generate_response(prompt).strip()
        st.session_state["past"].append(prompt)
        st.session_state["generated"].append(output)


INITIAL_MESSAGE = """
🧞‍♂ I am a mind reader with magical abilities! 🔮
🤔 Give me a category e.g. animal, or a famous person.
💬 I will ask questions and guess what you are thinking of!
"""

with response_container:
    message(INITIAL_MESSAGE)
    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            st.chat_message("user").write(st.session_state["past"][i])
            st.chat_message("ai").write(st.session_state["generated"][i])

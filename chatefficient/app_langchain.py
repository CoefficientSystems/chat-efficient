"""Streamlit app using LangChain + locally-running Vicuna.

Examples:
    $ streamlit run chatefficient/app_langchain.py
"""
import streamlit as st
from joblib import Memory
from langchain import LLMChain, PromptTemplate
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import LlamaCpp
from langchain.memory import ConversationBufferWindowMemory
from streamlit_chat import message

LOCATION = "./cachedir"
MEMORY = Memory(LOCATION, verbose=0)

# Callbacks support token-wise streaming
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Verbose is required to pass to the callback manager
n_gpu_layers = 40  # Change this value based on your model and your GPU VRAM pool.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
n_ctx = 512 * 2

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    n_ctx=n_ctx,
    # model_path="./models/llama-7b.ggmlv3.q4_0.bin",
    model_path="./models/ggml-vic13b-uncensored-q4_0.bin",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    callback_manager=callback_manager,
    verbose=True,
    pipeline_kwargs={"max_new_tokens": 64 * 4},
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
    You are a mind reader with magical abilities.
    You will be given something to guess, such as an animal, or a famous person.
    You will ask a question, I will provide an answer, and then you will guess.
    If your guess is wrong, then you must ask another question.
    Repeat this until you get the right answer.
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
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("You:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")

    if submit_button and user_input:
        output = generate_response(user_input).strip()
        st.session_state["past"].append(user_input)
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
            message(st.session_state["past"][i], is_user=True, key=f"{i}_user")
            message(st.session_state["generated"][i], key=f"{i}")

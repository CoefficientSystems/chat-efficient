"""Streamlit 101.

Docs:
- https://docs.streamlit.io/library/get-started
- https://docs.streamlit.io/library/api-reference/session-state
- https://discuss.streamlit.io/t/new-component-streamlit-chat-a-new-way-to-create-chatbots/20412

Examples:
    $ streamlit hello
    $ streamlit run chatefficient/streamlit_demo.py
"""

import numpy as np
import pandas as pd
import streamlit as st
from streamlit_chat import message

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})

######### Part 1: Magic Commands #########
df


######### Part 2: st.write() #########
st.write(df)


######### Part 3: Plotting Charts #########
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)


######### Part 4: Maps #########
old_street = [51.525, -0.088]
map_data = pd.DataFrame(np.random.randn(50, 2) / [150, 150] + old_street, columns=["lat", "lon"])
st.map(map_data)


######### Part 5: Widgets #########
x = st.slider("x")  # 👈 this is a widget
st.write(x, "squared is", x * x)

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
option = st.selectbox("Which number do you like best?", df["first column"])
"You selected: ", option


######### Part 6: Sidebar #########
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?", ("Email", "Home phone", "Mobile phone")
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))


######### Part 7: Session State #########
# Initialization
if "name" not in st.session_state:
    st.session_state["name"] = "DEFAULT NAME"

st.sidebar.text_input("Your name", key="name")

# You can access the value at any point with:
st.session_state.name


######### Part 8: Streamlit Chat #########
message("Hello human 👋")
message("Hey there bot!", is_user=True)  # align's the message to the right
message("Hope your webinar is going OK?")
message("Me too!", is_user=True)

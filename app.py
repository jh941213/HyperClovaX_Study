import streamlit as st
from clova import LlmClovaStudio
import base64

llm = LlmClovaStudio(
    host='https://clovastudio.stream.ntruss.com/',
    api_key='your api key',
    api_key_primary_val='your api key',
    request_id='your request id'
)

# Page configuration
st.set_page_config(
    page_title="🏴‍☠️ 루피봇 (with HyperClova X)",
    page_icon="🏴‍☠️",
    layout="wide"
)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title("🏴‍☠️ 루피봇 (with HyperClova X)")

def load_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

user_avatar_base64 = load_image("user.png")
assistant_avatar_base64 = load_image("luffy.png")

chat_container = st.container()
with chat_container:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        css_class = "user-message" if message["role"] == "user" else "assistant-message"
        avatar_base64 = user_avatar_base64 if message["role"] == "user" else assistant_avatar_base64
        avatar_url = f"data:image/png;base64,{avatar_base64}"
        st.markdown(
            f"""
            <div class='chat-message {css_class}'>
                <img src='{avatar_url}' class='avatar' />
                <div class='message-content'>{message['content']}</div>
            </div>
            """, unsafe_allow_html=True
        )


prompt = st.text_input("What is up?", key="chat_input", placeholder="Type your message here...", help="Enter your message to chat with 루피봇")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = llm._call(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})


    chat_container.empty()
    with chat_container:
        for message in st.session_state.messages:
            css_class = "user-message" if message["role"] == "user" else "assistant-message"
            avatar_base64 = user_avatar_base64 if message["role"] == "user" else assistant_avatar_base64
            avatar_url = f"data:image/png;base64,{avatar_base64}"
            st.markdown(
                f"""
                <div class='chat-message {css_class}'>
                    <img src='{avatar_url}' class='avatar' />
                    <div class='message-content'>{message['content']}</div>
                </div>
                """, unsafe_allow_html=True
            )

# Scroll to bottom
st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

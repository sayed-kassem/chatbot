import streamlit as st
from openai import OpenAI

# App title
st.set_page_config(page_title="🤗💬 HugChat")
# Credentials
with st.sidebar:
    st.title('🤗💬 HugChat')
    if ('EMAIL' in st.secrets) and ('PASS' in st.secrets):
        st.success('Login credentials already provided!', icon='✅')
        hf_email = st.secrets['EMAIL']
        hf_pass = st.secrets['PASS']
        api_key = st.secrets["OPENAI"]
        client = OpenAI(api_key=api_key)
    else:
        hf_email = st.text_input('Enter E-mail:', type='password')
        hf_pass = st.text_input('Enter password:', type='password')
        api_key = st.text_input("Enter OpenAi key:",type='password')
        client = OpenAI(api_key=api_key)
        
        if not (hf_email and hf_pass and client.api_key):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

# Store LLM generated responses
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "system", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating response
def generate_response(prompt_input, email, passwd):
    if(email and passwd):
        chat_completion = client.chat.completions.create(messages=[{"role":"user", "content": prompt_input}], model="gpt-3.5-turbo")
        return chat_completion.choices[0].message.content.strip()

# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "system":
    with st.chat_message("system"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "system", "content": response}
    st.session_state.messages.append(message)
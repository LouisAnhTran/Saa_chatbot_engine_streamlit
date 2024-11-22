import streamlit as st
import requests
from datetime import datetime

# FastAPI backend URL for fetching messages
API_URL = "http://localhost:8000/api/v1/sia_engine"
USER_NAME="louis"

# Streamlit app title
st.title("Saa Chatbot Version II")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

    # Fetch initial messages from FastAPI backend when app starts
    user_name = "louis"  # Replace with dynamic username if needed
    response = requests.get(f"{API_URL}/fetch_messages/{user_name}")
    
    if response.status_code == 200:
        # Extract the messages from the response and add them to session_state
        print("response: ",response)
        message = response.json()
        print("message before json: ",message)
        print("message: ",message['data'])
        st.session_state.messages.append({"role":"assistant","content":message['data'],"category_id":message['category_id']})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "Error fetching messages"})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Answer Saa questions..."):
    # Display user message in the chat
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt,"category_id":st.session_state.messages[-1]['category_id']})

    # Send the user's message to FastAPI backend for processing (example)
    response = requests.post(f"{API_URL}/generate_response/{USER_NAME}", json={"role":"user","content": prompt,"timestamp":str(datetime.now()),"category_id":st.session_state.messages[-1]['category_id']})

    if response.status_code == 200:
        assistant_message = response.json()
        print("assistant_mesage: ",assistant_message['data'])
    else:
        assistant_message = "Error: Unable to get response from backend"

    # Display assistant's response in the chat
    with st.chat_message("assistant"):
        st.markdown(assistant_message['data'])
    # Add assistant response to chat history

    print("assistant message: ",assistant_message)
    st.session_state.messages.append({"role": "assistant", "content": assistant_message['data'],"category_id":assistant_message['category_id']})

import streamlit as st
import random
import time
import requests
import json

### APPLICATION SETUP
api_gateway_endpoint = # ADD API GATEWAY ENDPOINT HERE
api_gateawy_api_key = # ADD YOUR API KEY HERE

### SUPPORTING FUNCTIONS
def call_API_Gateway(user_request):
    
    # defining request
    user_request_object = { "user_request": user_request }

    # make REST API Call to API Gateway using requests package
    response = requests.post(api_gateway_endpoint, json=user_request_object, headers={"x-api-key": api_gateawy_api_key})

    return response

### LLM APP
st.title("Call Center Co. LLM Chatbot - Task 2")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call API Gateway
    agent_response = call_API_Gateway(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = agent_response.text

        # # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            
            full_response += chunk + " "
            time.sleep(0.05)

            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")

        # Display response
        message_placeholder.markdown(assistant_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})



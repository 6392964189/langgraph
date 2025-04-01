import streamlit as st
import requests

# Set up the page title and layout
st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

# User-defined system prompt for AI agent
system_prompt = st.text_area("Define your AI Agent: ", height=70, placeholder="Type your system prompt here...")

# Groq Model Names
MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]

# Select provider (Groq)
provider = st.radio("Select Provider:", ("Groq",))

# Select model
selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)

# Option to allow web search
allow_web_search = st.checkbox("Allow Web Search")

# User query input
user_query = st.text_area("Enter your query: ", height=150, placeholder="Ask Anything!")

# API URL for backend
API_URL = "http://127.0.0.1:9999/chat"

# Button to ask the agent
if st.button("Ask Agent!"):
    if user_query.strip():
        # Prepare the payload for backend communication
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        # Make the request to the backend
        response = requests.post(API_URL, json=payload)
        
        # Check if the response was successful
        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {response_data}")

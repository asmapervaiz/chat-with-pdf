import streamlit as st
import requests
from streamlit_chat import message

API_BASE_URL = "http://127.0.0.1:8000"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    
st.set_page_config(page_title="PDF Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
    .chat-container {
        max-width: 700px;
        margin: auto;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📄 PDF Chatbot 🤖")


# Upload PDF Section
st.header("📤 Upload a PDF")


user_id = st.text_input("User ID:", placeholder="Enter your User ID...", key="upload_user_id")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], help="Upload a PDF to extract knowledge.")

if uploaded_file is not None and user_id:
    with st.spinner("🚀 Uploading and processing PDF..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
        response = requests.post(f"{API_BASE_URL}/upload/", params={"user_id": user_id}, files=files)
        if response.status_code == 200:
            st.success("✅ PDF uploaded and processed successfully!")
        else:
            st.error(f"❌ Error uploading PDF: {response.json().get('detail')}")
elif uploaded_file and not user_id:
    st.warning("⚠️ Please enter a User ID before uploading.")


# Chatbot Interaction Section
st.header("💬 Chat with Your PDF")

# Use a unique key for chat user input to prevent conflicts
user_input = st.text_input("Ask a question:", placeholder="Type your question here...", key="chat_user_input")

if st.button("Send"):
    if user_input:
        with st.spinner("🤖 Thinking..."):
            payload = {"user_id": user_id, "query": user_input}
            response = requests.post(f"{API_BASE_URL}/chat/", json=payload)
            if response.status_code == 200:
                answer = response.json().get("answer")
                st.session_state.chat_history.append((user_input, answer))
            else:
                st.error("❌ Error fetching answer. Please try again.")
    else:
        st.warning("⚠️ Please enter a question.")
        
        
# Display chat history
st.subheader("📜 Conversation History")
for i, (question, answer) in enumerate(st.session_state.chat_history):
    message(question, is_user=True, key=f"user_{i}")
    message(answer, is_user=False, key=f"bot_{i}")
    
    
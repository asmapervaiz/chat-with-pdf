# chat-with-pdf

This project is a PDF Chatbot application that allows users to upload PDF documents and interact with the content via an AI-powered chatbot. The backend is built with FastAPI, and the frontend is developed using Streamlit.

## Features

Upload PDFs: Easily upload PDF files to extract and analyze content.

Chat with PDFs: Ask questions and receive insights directly from your PDF documents.

User-Friendly Interface: Simple and interactive UI for seamless user experience.

## Technologies Used

FastAPI: For building the backend API.

Streamlit: For creating the interactive web interface.

OpenAI API: For AI-powered responses.

Docker: For containerization and easy deployment.

## Setup Instructions

Prerequisites

Python 3.8+

Docker (for containerization)

Git (for version control)

### 1. Clone the Repository

git clone https://github.com/asmapervaiz/chat-with-pdf.git

cd chat-with-pdf

### 2. Environment Variables

Create a .env file in the project root directory and add your OpenAI API key:

OPENAI_API_KEY= your openai key here

### 3. Install dependencies:

pip install -r requirements.txt

### 4. Run FastAPI Backend:

uvicorn api:app --reload

### 5. Run Streamlit Frontend:

streamlit run pdf_chatbot_ui.py

# API Documentation

## 1.Upload PDF

### Endpoint: 
/upload/

### Method: POST

### Parameters:

user_id: User identifier (required).

Body: PDF file (multipart/form-data).

Response: Success or error message.

## 2.Chat with PDF

### Endpoint: 
/chat/

### Method: POST

### Body:
{
  "user_id": "<user_id>",
  "query": "<your_question>"
}

## Response: 
AI-generated answer based on the PDF content.

# Project Structure

![image](https://github.com/user-attachments/assets/7f30eb51-ce38-42f3-9331-faf412105106)

# License

This project is licensed under the MIT License.

# Contributing

Feel free to open issues or submit pull requests to improve the project.

# Acknowledgments

Thanks to OpenAI for providing the AI model.

Developed by Asma Pervaiz 🚀


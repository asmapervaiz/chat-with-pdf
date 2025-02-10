from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import fitz  
import faiss
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI 
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from typing import Dict, List
from openai import OpenAI 
from langchain.schema import Document  

load_dotenv()

app = FastAPI()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  


user_data: Dict[str, FAISS] = {}
chat_histories: Dict[str, List[Dict[str, str]]] = {}

def extract_text_from_pdf(file: UploadFile):
    text = ""
    try:
        with fitz.open(stream=file.file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")
    return text

def add_text_to_vector_store(user_id: str, text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks]
    embeddings = OpenAIEmbeddings()

    if user_id not in user_data:
        user_data[user_id] = FAISS.from_documents(documents, embedding=embeddings)
    else:
        user_data[user_id].add_documents(documents)

class ChatRequest(BaseModel):
    user_id: str
    query: str

@app.post("/upload/")
async def upload_pdf(user_id: str, file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    text = extract_text_from_pdf(file)
    add_text_to_vector_store(user_id, text)
    return {"message": "PDF uploaded and processed successfully."}

@app.post("/chat/")
async def chat(request: ChatRequest):
    user_id, query = request.user_id, request.query

    if user_id not in user_data:
        raise HTTPException(status_code=400, detail="No uploaded documents found for this user.")

    relevant_docs = user_data[user_id].similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    messages = chat_histories.get(user_id, [])
    messages.append({"role": "user", "content": query})

    prompt = f"Answer the question based on the following context:\n{context}\n\nQuestion: {query}"
    response = openai_client.chat.completions.create(  # Updated API call
        model="gpt-4o-mini",  # Updated to the latest model
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            *messages,
            {"role": "user", "content": prompt}
        ]
    )
    answer = response.choices[0].message.content  # Updated response handling

    messages.append({"role": "assistant", "content": answer})
    chat_histories[user_id] = messages  # Save chat history

    return {"answer": answer, "history": messages}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

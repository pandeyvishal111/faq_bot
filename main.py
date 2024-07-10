import json
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index and Q&A pairs
index = faiss.read_index('knowledge_base_index.faiss')
with open('qa_pairs.json', 'r') as f:
    qa_pairs = json.load(f)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def get_answer(request: Request, question: str = Form(...)):
    # Generate embedding for the user question
    question_embedding = model.encode([question])
    
    # Search for the closest embedding in the FAISS index
    D, I = index.search(np.array(question_embedding), 1)
    most_similar_index = I[0][0]
    
    # Retrieve the most similar Q&A pair
    best_match = qa_pairs[most_similar_index]
    answer = best_match['answer']
    
    return templates.TemplateResponse("index.html", {"request": request,"question":question,"answer":answer})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

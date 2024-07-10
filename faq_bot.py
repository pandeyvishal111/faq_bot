import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import spacy
import logging

# Initialize spaCy NLP model
nlp = spacy.load('en_core_web_sm')

# Initialize FastAPI app
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Setup logging
logging.basicConfig(filename='faq_bot.log', level=logging.INFO)

# Fetch and parse the knowledge base
def fetch_knowledge_base(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text(separator='\n')
    return content

# Preprocess the content and create a list of sentences
def preprocess_content(content):
    doc = nlp(content)
    sentences = [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 0]
    return sentences

# Find the most similar question in the knowledge base
def find_most_similar_question(user_question, knowledge_base):
    user_question_doc = nlp(user_question)
    similarities = [(question, user_question_doc.similarity(nlp(question))) for question in knowledge_base]
    most_similar_question = max(similarities, key=lambda item: item[1])
    return most_similar_question[0]

# Fetch content from the knowledge base
url = 'https://knowledge.hrone.cloud/?access_token=8f0b5d8f12dd7282ea8f0c4e4f2609d9040be746b9a6233bfdee40333d069365'
knowledge_base_content = fetch_knowledge_base(url)
knowledge_base = preprocess_content(knowledge_base_content)

# Define FastAPI routes
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def get_answer(request: Request, question: str = Form(...)):
    most_similar_question = find_most_similar_question(question, knowledge_base)
    answer = f"Similar Question: {most_similar_question}"
    logging.info(f"Q: {question} | A: {answer}")
    return templates.TemplateResponse("index.html", {"request": request, "question": question, "answer": answer})

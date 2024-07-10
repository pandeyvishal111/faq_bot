from knowledge import *
from transformer import *
from embeddings import *


# Fetch content from the knowledge base
url = 'https://knowledge.hrone.cloud/?access_token=8f0b5d8f12dd7282ea8f0c4e4f2609d9040be746b9a6233bfdee40333d069365'
paragraphs = fetch_knowledge_base(url)


#Use LLM to Create Q&A Pairs
qna_pairs = generate_qa_pairs(paragraphs)

response = generate_embeddings(qna_pairs)

if response == 'Success':
    print("Embeddings saved successfully")
else:
    print(f"There was an error {response}")
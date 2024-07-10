from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load the pre-trained model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2',device='cpu')

# Generate embeddings for the Q&A pairs
def generate_embeddings(qa_pairs):
    # Generate embeddings for the Q&A pairs
    questions = [pair['question'] for pair in qa_pairs]
    question_embeddings = model.encode(questions)

    # Create a FAISS index
    dimension = question_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Add question embeddings to the index
    index.add(np.array(question_embeddings))

    # Save the index and Q&A pairs
    faiss.write_index(index, 'knowledge_base_index.faiss')
    with open('qa_pairs.json', 'w') as f:
        json.dump(qa_pairs, f)
    return 'Success'
    
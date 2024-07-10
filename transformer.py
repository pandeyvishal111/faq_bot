from transformers import pipeline

# Initialize the Hugging Face pipeline for Q&A
qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

# Generate Q&A pairs
def generate_qa_pairs(paragraphs):
    qna_pairs = []
    paragraph = '.'.join(paragraphs)
    if len(paragraph.strip()) > 0:
        # For simplicity, we're using static questions here; we can improve this with a more dynamic approach
        questions = [
            "Why is HCM software important for HR professionals?",
            "How does HCM software simplify the life of HR and employees?",
            "What makes HCM software efficient and intuitive?",
            "What mission drives the creation of HR automation software?",
            "How does HR automation software help HR professionals explore their true potential?",
            "What types of tasks can HR automation software eliminate?",
            "What benefits do HR professionals gain from using value-driven HR automation software?",
            "How does HR automation software free up time and mental space for HR professionals?",
            "Why should HR professionals avoid managing administrative tasks manually?",
            "What features should an HR automation software have to be considered simple and effective?"
        ]
        for question in questions:
            result = qa_pipeline(question=question, context=paragraph)
            qna_pairs.append({
                'question': question,
                'answer': result['answer']
            })
    return qna_pairs

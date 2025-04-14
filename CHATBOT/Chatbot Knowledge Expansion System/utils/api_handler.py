import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_embeddings(texts):
    """Get embeddings using Gemini API"""
    if isinstance(texts, str):
        texts = [texts]
    
    model = genai.GenerativeModel('models/embedding-001')
    embeddings = []
    for text in texts:
        response = model.embed_content(text)
        embeddings.append(response['embedding'])
    return embeddings

def generate_response(prompt, context):
    """Generate chatbot response using Gemini"""
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"Context: {context}\n\nQuestion: {prompt}")
    return response.text
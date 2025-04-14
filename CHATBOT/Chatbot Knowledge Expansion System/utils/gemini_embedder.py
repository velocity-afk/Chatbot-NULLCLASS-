import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def get_embeddings(texts):
    """Get embeddings using Gemini API"""
    model = genai.GenerativeModel('models/embedding-001')
    if isinstance(texts, str):
        return model.embed_content(texts)['embedding']
    return [model.embed_content(text)['embedding'] for text in texts]
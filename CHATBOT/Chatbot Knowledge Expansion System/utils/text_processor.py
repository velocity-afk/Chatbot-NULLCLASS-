from nltk.tokenize import sent_tokenize
import nltk
import re

nltk.download('punkt', quiet=True)

class TextProcessor:
    def clean_text(self, text):
        """Clean and preprocess text"""
        text = re.sub(r'[^\w\s.,!?]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def split_into_chunks(self, text, max_length=512):
        """Split text into meaningful chunks"""
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
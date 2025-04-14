from textblob import TextBlob
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        try:
            # Try the newest model first, fallback to others
            self.gemini = genai.GenerativeModel('gemini-1.5-pro-latest')
        except:
            try:
                self.gemini = genai.GenerativeModel('gemini-pro')
            except:
                self.gemini = None
        
    def analyze(self, text):
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        
        if polarity > 0.2:
            return "positive"
        elif polarity < -0.2:
            return "negative"
        else:
            return "neutral"
    
    def get_emotional_response(self, sentiment, answer):
        if not self.gemini:
            return answer  # Fallback if no Gemini available
            
        try:
            prompts = {
                "positive": f"User seems happy. Make this response cheerful: {answer}",
                "negative": f"User seems upset. Make this empathetic: {answer}",
                "neutral": answer
            }
            response = self.gemini.generate_content(prompts[sentiment])
            return response.text
        except Exception as e:
            print(f"Sentiment adaptation failed, using plain response: {str(e)}")
            return answer
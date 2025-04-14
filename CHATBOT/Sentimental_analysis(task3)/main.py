from knowledge import KnowledgeBase
from sentiment import SentimentAnalyzer
import os
import time

class ChatBot:
    def __init__(self):
        print("Initializing chatbot...")
        self.knowledge_base = KnowledgeBase()
        self.sentiment_analyzer = SentimentAnalyzer()
        
        # Load knowledge with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.knowledge_base.load_sources()
                break
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    print("Failed to load knowledge base")
                time.sleep(2)
    
    def respond(self, user_input):
        try:
            # Get basic answer
            answer = self.knowledge_base.query(user_input)
            
            # Skip sentiment for greetings
            if user_input.lower() in ('hi', 'hello', 'how are you'):
                return "I'm an AI assistant. How can I help you today?"
                
            # Analyze and adapt
            sentiment = self.sentiment_analyzer.analyze(user_input)
            return self.sentiment_analyzer.get_emotional_response(sentiment, answer)
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("ERROR: Missing GEMINI_API_KEY in .env file")
        exit(1)
        
    bot = ChatBot()
    print("\nChatbot ready! Type 'quit' to exit.")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ('quit', 'exit'):
                break
                
            response = bot.respond(user_input)
            print(f"Bot: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"System error: {str(e)}")
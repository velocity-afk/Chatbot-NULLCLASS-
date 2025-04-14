import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# Load environment
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class KnowledgeBot:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Updated model name
        self.knowledge = []
        
    def add_source(self, content):
        """Add text content to knowledge base"""
        if content and len(content) > 10:  # Basic validation
            self.knowledge.append(content)
        
    def scrape_website(self, url):
        """Get clean text from a webpage"""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                element.decompose()
                
            return ' '.join(soup.stripped_strings)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
            
    def load_sources(self, filename="C:/Users/Aphilip/Documents/Chatbot Knowledge Expansion System/data/sources.txt"):
        """Load from text file with URLs or file paths"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for source in f:
                    source = source.strip()
                    if not source:
                        continue
                        
                    if source.startswith(('http://', 'https://')):
                        content = self.scrape_website(source)
                    else:
                        try:
                            with open(source, 'r', encoding='utf-8') as file:
                                content = file.read()
                        except Exception as e:
                            print(f"Error reading {source}: {e}")
                            content = None
                            
                    self.add_source(content)
            print(f"Loaded {len(self.knowledge)} knowledge sources")
        except FileNotFoundError:
            print(f"Error: {filename} not found")
    
    def ask(self, question):
        """Get answer using knowledge base"""
        if not self.knowledge:
            return "Error: No knowledge loaded. Please check sources.txt"
            
        try:
            # Combine most relevant knowledge (first 3 sources)
            context = "\n\n".join([
                f"Source {i+1}:\n{knowledge[:2000]}..." if len(knowledge) > 2000 
                else knowledge 
                for i, knowledge in enumerate(self.knowledge[:3])
            ])
            
            prompt = f"""Use the following context to answer the question:
            
            Context:
            {context}
            
            Question: {question}
            
            Provide a concise, accurate answer based only on the given context."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {str(e)}"

if __name__ == "__main__":
    print("Initializing Knowledge Bot...")
    bot = KnowledgeBot()
    bot.load_sources()
    
    print("\nKnowledge Bot Ready! (Type 'quit' to exit)")
    while True:
        try:
            question = input("\nYour question: ").strip()
            if not question:
                continue
            if question.lower() in ('quit', 'exit'):
                break
                
            answer = bot.ask(question)
            print(f"\nAnswer: {answer}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
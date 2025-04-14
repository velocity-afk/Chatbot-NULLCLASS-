import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class KnowledgeBase:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        self.knowledge = []
        
    def add_source(self, content):
        if content and len(content) > 10:
            self.knowledge.append(content)
        
    def scrape_website(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'footer']):
                element.decompose()
                
            return ' '.join(soup.stripped_strings)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
            
    def load_sources(self, filename="C:/Users/Aphilip/Documents/Sentimental_analysis(task3)/data/sources.txt"):
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
    
    def query(self, question):
        if not self.knowledge:
            return "Error: No knowledge loaded"
            
        context = "\n\n".join(self.knowledge[:3])
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
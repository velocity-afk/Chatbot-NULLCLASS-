import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Vector Database Configuration
VECTOR_DB_PATH = "data/knowledge_base"
COLLECTION_NAME = "chatbot_knowledge"

# Update Schedule (in hours)
UPDATE_FREQUENCY = 24

# Information Sources
SOURCES_FILE = "C:/Users/Aphilip/Documents/Chatbot Knowledge Expansion System/data/sources.txt"

# Information Sources (file paths or URLs)
#SOURCES_FILE = "C:/Users/Aphilip/Documents/Chatbot Knowledge Expansion System/data/sources.txt"
import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, "data", "database.db")

# Ollama LLM Configuration
# Make sure this URL matches your locally running endpoint.
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3"  # Ensure this is exactly the model name your instance expects

# LLM parameters
MAX_TOKENS = 150
TEMPERATURE = 0

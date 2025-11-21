import groq
from app.config import settings

def get_available_models():
    """Get list of available models from Groq API"""
    try:
        client = groq.Client(api_key=settings.GROQ_API_KEY)
        models = client.models.list()
        
        available_models = []
        for model in models.data:
            if hasattr(model, 'id'):
                available_models.append(model.id)
        
        print("Available Groq models:", available_models)
        return available_models
        
    except Exception as e:
        print(f"Error fetching available models: {e}")
        # Fallback to known working models
        return [
            "llama-3.1-8b-instant",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ]

# Test the available models
if __name__ == "__main__":
    models = get_available_models()
    print("Available models:", models)
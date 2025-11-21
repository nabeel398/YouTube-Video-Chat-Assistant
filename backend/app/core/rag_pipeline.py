from app.core.vector_store import search_index
from app.core.efficient_groq import ask_groq_quality
import re

def enforce_word_limit(text, max_words=20):
    """Enforce word limit with smart truncation"""
    words = text.split()
    if len(words) > max_words:
        truncated = " ".join(words[:max_words])
        if not truncated.endswith(('.', '!', '?')):
            truncated += "..."
        return truncated
    return text

def generate_quality_answer(query, chunks, index):
    """Always use LLM for quality answers with 20-word limit"""
    # Search for relevant chunks
    retrieved_chunks = search_index(query, index, chunks, top_k=3)
    
    if not retrieved_chunks:
        return "I couldn't find relevant information in the video."
    
    # Prepare context for LLM
    context = " ".join(retrieved_chunks)
    
    # ALWAYS use LLM for quality answers
    llm_answer = ask_groq_quality(context, query)
    
    return llm_answer

# Keep this for backward compatibility
def generate_answer(query, chunks, index):
    return generate_quality_answer(query, chunks, index)
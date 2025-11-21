from langchain_groq import ChatGroq
from app.config import settings
import re

class EfficientGroqClient:
    def __init__(self):
        self.llm = None
        # Updated model names - use currently available models
        self.available_models = [
            "llama-3.1-8b-instant",    # Fast and efficient
            "llama-3.1-70b-versatile", # More powerful
            "mixtral-8x7b-32768",      # High quality
            "gemma2-9b-it"             # Alternative option
        ]
        self.current_model = self.available_models[0]  # Default to fastest
        self.max_context_length = 1500
        self.cache = {}
        self.usage_count = 0
        self.max_daily_usage = 1000
        self.max_answer_words = 30
    
    def get_llm(self):
        if self.llm is None:
            try:
                self.llm = ChatGroq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name=self.current_model,
                    temperature=0.1,
                    max_tokens=150,
                )
            except Exception as e:
                # If first model fails, try others
                print(f"Model {self.current_model} failed, trying alternatives...")
                self.try_alternative_models()
        return self.llm
    
    def try_alternative_models(self):
        """Try alternative models if the current one fails"""
        for model in self.available_models[1:]:
            try:
                print(f"Trying model: {model}")
                self.llm = ChatGroq(
                    groq_api_key=settings.GROQ_API_KEY,
                    model_name=model,
                    temperature=0.1,
                    max_tokens=150,
                )
                self.current_model = model
                print(f"Successfully switched to model: {model}")
                return
            except Exception as e:
                print(f"Model {model} also failed: {e}")
                continue
        
        raise Exception("All Groq models failed. Please check available models.")
    
    def compress_context(self, context):
        """Reduce context size to save tokens"""
        if len(context) <= self.max_context_length:
            return context
        
        half = self.max_context_length // 2
        return context[:half] + " ... " + context[-half:]
    
    def enforce_word_limit(self, text):
        """Strict 30-word maximum limit"""
        words = text.split()
        if len(words) > self.max_answer_words:
            truncated = " ".join(words[:self.max_answer_words])
            if not truncated.endswith(('.', '!', '?')):
                truncated += "..."
            return truncated
        return text
    
    def ask_with_quality(self, context, question):
        """Always use LLM for quality answers, but limit to 30 words"""
        if self.usage_count >= self.max_daily_usage:
            return "Daily limit reached. Please try again later."
        
        cache_key = f"{question[:50]}_{hash(context) % 10000}"
        
        if cache_key in self.cache:
            self.usage_count += 1
            return self.cache[cache_key]
        
        try:
            llm = self.get_llm()
            compressed_context = self.compress_context(context)
            
            prompt = f"""Based ONLY on the YouTube transcript below, provide a HIGH-QUALITY answer to the question.
IMPORTANT: Answer must be UNDER 30 WORDS. Be concise but informative.

TRANSCRIPT: {compressed_context}

QUESTION: {question}

CONCISE HIGH-QUALITY ANSWER (UNDER 30 WORDS):"""
            
            response = llm.invoke(prompt)
            answer = response.content.strip()
            
            # Strict enforcement of word limit
            answer = self.enforce_word_limit(answer)
            
            self.cache[cache_key] = answer
            self.usage_count += 1
            
            return answer
            
        except Exception as e:
            print(f"Groq API Error: {e}")
            return f"AI service temporarily unavailable. Please try again."
    
    def get_usage_stats(self):
        return {
            "used_today": self.usage_count,
            "daily_limit": self.max_daily_usage,
            "remaining": self.max_daily_usage - self.usage_count,
            "max_words_per_answer": self.max_answer_words,
            "current_model": self.current_model,
            "available_models": self.available_models
        }
    
    def reset_usage(self):
        self.usage_count = 0
        self.cache.clear()

# Global instance
groq_client = EfficientGroqClient()

def ask_groq_quality(context, question):
    return groq_client.ask_with_quality(context, question)
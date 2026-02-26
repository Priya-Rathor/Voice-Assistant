import google.generativeai as genai
from config import GOOGLE_API_KEY, MODEL_NAME, TEMPERATURE

class VoiceAssistant:
    """Core voice assistant logic using Google Gemini."""
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Initialize the model
        generation_config = {
            "temperature": TEMPERATURE,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 1024,
        }
        
        self.model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config=generation_config,
        )
        
        # Start chat session
        self.chat = self.model.start_chat(history=[])
        
        # Set system instruction
        self.system_message = """My name is THE ENTITY. You are a helpful voice assistant.

Always begin every response with:
"How can I help you?"

Guidelines:
- Provide complete, natural responses.
- Keep answers conversational yet thorough.
- Always finish sentences clearly and completely.
- Speak in a friendly and clear manner.
"""

    
    def process_query(self, text):
        """Process user query and generate response."""
        try:
            # Send message with system context
            full_prompt = f"{self.system_message}\n\nUser: {text}\nAssistant:"
            
            response = self.chat.send_message(full_prompt)
            assistant_response = response.text
            
            return assistant_response
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return "I'm sorry, I encountered an error. Please try again."
    
    def reset_conversation(self):
        """Reset conversation history."""
        self.chat = self.model.start_chat(history=[])
import pyttsx3
import os
from config import AUDIO_DIR

class TextToSpeech:
    """Handle text-to-speech conversion using local TTS."""
    
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            self.engine.setProperty('rate', 160)  # Slightly faster for better clarity
            self.engine.setProperty('volume', 1.0)  # Full volume
            
            # Try to set a better voice (prefer female voices for clarity)
            voices = self.engine.getProperty('voices')
            if len(voices) > 0:
                # Try to find a good English voice
                for voice in voices:
                    if 'english' in voice.name.lower() or 'en' in voice.languages:
                        self.engine.setProperty('voice', voice.id)
                        print(f"Using voice: {voice.name}")
                        break
                else:
                    # Use first voice as fallback
                    self.engine.setProperty('voice', voices[0].id)
                    print(f"Using default voice: {voices[0].name}")
            
            print("✓ Text-to-speech ready!")
                
        except Exception as e:
            print(f"Error initializing TTS: {e}")
            self.engine = None
    
    def speak(self, text):
        """Convert text to speech and play."""
        if self.engine is None:
            print(f"⚠️  TTS not available. Text: {text}")
            return
        
        if not text or len(text.strip()) == 0:
            print("⚠️  No text to speak")
            return
            
        try:
            # Clean the text for better speech
            text = text.strip()
            
            # Debug: Show what we're trying to say
            print(f"🔊 TTS Output: {text}")
            
            self.engine.say(text)
            self.engine.runAndWait()
            
            print("✓ Speech completed")
            
        except Exception as e:
            print(f"❌ Error speaking: {e}")
            import traceback
            traceback.print_exc()
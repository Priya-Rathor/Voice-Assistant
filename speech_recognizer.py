import speech_recognition as sr
from config import LANGUAGE

class SpeechRecognizer:
    """Handle speech-to-text conversion."""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        print("Adjusting for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Ready!")
    
    def listen(self, timeout=5, phrase_time_limit=10):
        """Listen for speech and convert to text."""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio, language=LANGUAGE)
            return text
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition: {e}")
            return None
    
    def listen_continuous(self, callback):
        """Continuously listen and call callback with text."""
        while True:
            text = self.listen()
            if text:
                callback(text)
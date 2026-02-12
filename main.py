from speech_recognizer import SpeechRecognizer
from text_to_speech import TextToSpeech
from assistant import VoiceAssistant
import sys

def main():
    """Main function."""
    print("=" * 60)
    print("🎤 I'm THE ENTITY (Powered by Google Gemini)")
    print("=" * 60)
    
    # Initialize components
    print("\nInitializing components...")
    
    try:
        print("- Initializing speech recognizer...")
        recognizer = SpeechRecognizer()
        
        print("- Initializing text-to-speech...")
        tts = TextToSpeech()
        
        print("- Initializing Gemini AI assistant...")
        assistant = VoiceAssistant()
        
        print("\n✓ All components ready!")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {e}")
        print("Please check your GOOGLE_API_KEY in .env file")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Instructions:")
    print("- Speak clearly into your microphone")
    print("- Say 'quit', 'exit', or 'stop' to end the session")
    print("- Say 'reset' to clear conversation history")
    print("=" * 60)
    print()
    
    # Welcome message
    tts.speak("Hello! I'm THE ENTITY. How can I help you today?")
    
    while True:
        try:
            # Listen for speech
            text = recognizer.listen()
            
            if not text:
                continue
            
            print(f"\n👤 You: {text}")
            
            # Check for exit commands
            if text.lower() in ['quit', 'exit', 'stop', 'goodbye']:
                response = "Goodbye! Have a great day!"
                print(f"🤖 Assistant: {response}")
                tts.speak(response)
                print("\n👋 Session ended")
                break
            
            # Check for reset command
            if text.lower() in ['reset', 'clear', 'start over']:
                assistant.reset_conversation()
                response = "Conversation history cleared. How can I help you?"
                print(f"🤖 Assistant: {response}")
                tts.speak(response)
                continue
            
            # Process query
            print("🤖 Thinking...")
            response = assistant.process_query(text)
            print(f"🤖 Assistant: {response}")
            
            # Speak response
            print("🔊 Speaking...")
            tts.speak(response)
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            tts.speak("Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()
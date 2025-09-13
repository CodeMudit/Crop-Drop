import requests
import json
from google.cloud import speech_v1p1beta1 as speech

API_KEY = "AIzaSyCp4awTqgjl7hUfY_iecS-CbfG81_Aa784"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

SYSTEM_INSTRUCTION = {
    "parts": [{
        "text": "You are a world-class agricultural expert chatbot named 'Crop Drop'. Your purpose is to provide highly specific, practical, and detailed advice on all aspects of agriculture. Your topics of expertise include crop cultivation, suitable soil types, water and sunlight requirements, specific fertilizer recommendations, pest and disease identification and treatment, and general farming techniques. All your responses must be grounded in agricultural science and be easy to understand for a farmer. Keep your answers concise and to the point, providing only the most essential and relevant information. You must respond in the same language that the user asks their question in. When the user asks in Hinglish, ensure the entire response is in colloquial, mixed-language Hinglish. You can also respond in Hindi, Punjabi, and English. Do not answer questions outside of agriculture. If a question is not related to agriculture, politely decline and redirect the user to ask a farming-related question."
    }]
}

def get_gemini_response(user_query):
    """
    Sends the user's query to the Gemini API and retrieves the response.
    """
    payload = {
        "contents": [{
            "parts": [{
                "text": user_query
            }]
        }],
        "systemInstruction": SYSTEM_INSTRUCTION
    }

    try:
        response = requests.post(API_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        response.raise_for_status()  # Check for HTTP errors

        result = response.json()
        
        bot_response_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text')
        
        if bot_response_text:
            return bot_response_text
        else:
            return "Sorry, I couldn't get a response. Please try again."
            
    except requests.exceptions.RequestException as e:
        return f"An error occurred while connecting to the API: {e}"
    except (json.JSONDecodeError, KeyError) as e:
        return f"An error occurred while parsing the API response: {e}"

def transcribe_audio(audio_content: bytes, lang: str = None) -> tuple[str, str]:
    """
    Transcribes audio to text using Google Cloud Speech-to-Text.
    Returns (transcript, detected_language).
    """
    client = speech.SpeechClient()

    # Configure recognition with Hindi optimization
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Adjust for MP3 if needed
        sample_rate_hertz=16000,  # Standard rate
        language_code='hi-IN',  # Explicitly set Hindi
        enable_automatic_punctuation=True,
        use_enhanced=True,  # Use enhanced model for better accuracy
        model='latest_long'  # Switch to long model for better context
    )

    audio = speech.RecognitionAudio(content=audio_content)

    try:
        response = client.recognize(config=config, audio=audio)
        if response.results:
            transcript = response.results[0].alternatives[0].transcript
            detected_lang = response.results[0].language_code
            return transcript, detected_lang
        else:
            return "No speech detected.", 'en-US'  # Fallback
    except Exception as e:
        print(f"STT failed: {e}")
        return "Transcription failed.", 'en-US'
def main():
    """
    Runs the main loop for the chatbot.
    """
    print("Hello! I am Crop Drop, your personal agriculture expert.")
    print("You can ask me about crops, soil, diseases, and much more.")
    print("I can answer in multiple languages like Hindi, Punjabi, English, and Hinglish.")
    print("---")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Thank you for using the chatbot! Goodbye!")
            break
        
        print("Crop Drop: Thinking...")
        response = get_gemini_response(user_input)
        print("Crop Drop:", response)
        print("---")

if __name__ == "__main__":
    main()
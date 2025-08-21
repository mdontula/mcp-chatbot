#!/usr/bin/env python3
"""
Test script for Google Cloud Speech APIs
"""

import os
from dotenv import load_dotenv
from services.speech_service import SpeechService
from config import Config

def test_speech_apis():
    """Test the speech service functionality"""
    print("🎤 Testing Google Cloud Speech APIs...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Validate configuration
    print("🔍 Validating configuration...")
    api_valid = Config.validate_api_keys()
    print(f"API Keys: {'✅ Valid' if api_valid else '❌ Invalid'}")
    
    google_valid = Config.validate_google_cloud()
    print(f"Google Cloud: {'✅ Valid' if google_valid else '❌ Invalid'}")
    
    if not google_valid:
        print("❌ Google Cloud validation failed. Cannot proceed with speech tests.")
        return False
    
    print("\n✅ Google Cloud credentials validated successfully!")
    
    # Test speech service
    try:
        print("\n🧪 Testing Speech Service...")
        speech_service = SpeechService()
        
        # Test 1: Get supported languages
        print("\n1️⃣ Testing supported languages...")
        languages_result = speech_service.get_supported_languages()
        if languages_result['success']:
            print(f"✅ Supported languages: {len(languages_result['languages'])} found")
            print(f"   Sample languages: {languages_result['languages'][:5]}")
        else:
            print(f"❌ Failed to get languages: {languages_result['error']}")
        
        # Test 2: Get available voices
        print("\n2️⃣ Testing available voices...")
        voices_result = speech_service.get_available_voices("en-US")
        if voices_result['success']:
            print(f"✅ Available voices: {len(voices_result['voices'])} found")
            print(f"   Sample voices: {[v['name'] for v in voices_result['voices'][:3]]}")
        else:
            print(f"❌ Failed to get voices: {voices_result['error']}")
        
        # Test 3: Text-to-speech (simple test)
        print("\n3️⃣ Testing text-to-speech...")
        test_text = "Hello! This is a test of the text to speech service."
        tts_result = speech_service.text_to_speech(test_text, "en-US-Standard-A", "en-US", "mp3")
        
        if tts_result['success']:
            print(f"✅ Text-to-speech successful!")
            print(f"   Text: {tts_result['text']}")
            print(f"   Voice: {tts_result['voice']}")
            print(f"   Format: {tts_result['format']}")
            print(f"   Audio data length: {len(tts_result['audio_data'])} characters")
        else:
            print(f"❌ Text-to-speech failed: {tts_result['error']}")
        
        print("\n🎉 Speech service tests completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing speech service: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_speech_apis()
    if success:
        print("\n✅ All tests passed! Your speech service is ready to use.")
        print("🚀 You can now start the speech chatbot with: python speech_chatbot.py")
    else:
        print("\n❌ Some tests failed. Please check your configuration.")

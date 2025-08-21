#!/usr/bin/env python3
"""
Speech Service
Handles speech-to-text and text-to-speech using Google Cloud APIs
"""

import os
import base64
import tempfile
from typing import Dict, Optional, Tuple
from google.cloud import speech_v1, texttospeech
from google.cloud.speech_v1 import RecognitionAudio, RecognitionConfig
from google.cloud.texttospeech import SynthesisInput, VoiceSelectionParams, AudioConfig
import wave
import io

class SpeechService:
    """Service for speech-to-text and text-to-speech operations"""
    
    def __init__(self):
        # Initialize Google Cloud clients
        self.speech_client = speech_v1.SpeechClient()
        self.tts_client = texttospeech.TextToSpeechClient()
        
        # Default audio settings
        self.default_language = "en-US"
        self.default_voice = "en-US-Standard-A"
        self.default_audio_encoding = texttospeech.AudioEncoding.MP3
        
    def speech_to_text(self, audio_data: bytes, language: str = "en-US", audio_format: str = "webm_opus") -> Dict:
        """
        Convert speech audio to text
        
        Args:
            audio_data: Raw audio data
            language: Language code (e.g., 'en-US', 'es-ES')
            audio_format: Audio format hint for better recognition
            
        Returns:
            Dictionary with transcription result or error
        """
        try:
            # Determine encoding based on format
            if audio_format == "webm_opus" or "opus" in audio_format:
                encoding = RecognitionConfig.AudioEncoding.WEBM_OPUS
            elif audio_format == "webm":
                encoding = RecognitionConfig.AudioEncoding.WEBM_OPUS
            elif audio_format == "mp4":
                encoding = RecognitionConfig.AudioEncoding.MP3
            elif audio_format == "wav":
                encoding = RecognitionConfig.AudioEncoding.LINEAR16
            else:
                # Default to auto-detection
                encoding = RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
            
            # Configure recognition - let Google Cloud auto-detect sample rate
            config = RecognitionConfig(
                encoding=encoding,
                language_code=language,
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                enable_word_confidence=True,
                # Remove sample_rate_hertz to let Google Cloud auto-detect
            )
            
            # Create recognition audio
            audio = RecognitionAudio(content=audio_data)
            
            # Perform recognition
            response = self.speech_client.recognize(config=config, audio=audio)
            
            if response.results:
                # Get the most confident result
                result = response.results[0]
                if result.alternatives:
                    transcript = result.alternatives[0].transcript
                    confidence = result.alternatives[0].confidence
                    
                    return {
                        "success": True,
                        "transcript": transcript,
                        "confidence": confidence,
                        "language": language
                    }
            
            return {
                "success": False,
                "error": "No speech detected or recognition failed"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Speech recognition error: {str(e)}"
            }
    
    def text_to_speech(self, text: str, voice: str = "en-US-Standard-A", 
                       language: str = "en-US", audio_format: str = "mp3") -> Dict:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            voice: Voice name (e.g., 'en-US-Standard-A', 'en-US-Standard-B')
            language: Language code (e.g., 'en-US', 'es-ES')
            audio_format: Output format ('mp3', 'wav', 'ogg')
            
        Returns:
            Dictionary with audio data or error
        """
        try:
            # Set up synthesis input
            synthesis_input = SynthesisInput(text=text)
            
            # Configure voice
            voice_params = VoiceSelectionParams(
                language_code=language,
                name=voice
            )
            
            # Configure audio output
            if audio_format.lower() == "mp3":
                audio_encoding = texttospeech.AudioEncoding.MP3
            elif audio_format.lower() == "wav":
                audio_encoding = texttospeech.AudioEncoding.LINEAR16
            elif audio_format.lower() == "ogg":
                audio_encoding = texttospeech.AudioEncoding.OGG_OPUS
            else:
                audio_encoding = texttospeech.AudioEncoding.MP3
            
            audio_config = AudioConfig(
                audio_encoding=audio_encoding,
                speaking_rate=1.0,
                pitch=0.0
            )
            
            # Perform synthesis
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice_params,
                audio_config=audio_config
            )
            
            # Encode audio data
            audio_b64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            return {
                "success": True,
                "audio_data": audio_b64,
                "format": audio_format,
                "text": text,
                "voice": voice,
                "language": language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Text-to-speech error: {str(e)}"
            }
    
    def get_available_voices(self, language: str = "en-US") -> Dict:
        """
        Get available voices for a language
        
        Args:
            language: Language code
            
        Returns:
            Dictionary with available voices
        """
        try:
            voices = self.tts_client.list_voices(language_code=language)
            
            voice_list = []
            for voice in voices.voices:
                voice_list.append({
                    "name": voice.name,
                    "language_codes": list(voice.language_codes),
                    "ssml_gender": voice.ssml_gender.name,
                    "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
                })
            
            return {
                "success": True,
                "voices": voice_list,
                "language": language
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting voices: {str(e)}"
            }
    
    def get_supported_languages(self) -> Dict:
        """
        Get list of supported languages
        
        Returns:
            Dictionary with supported languages
        """
        try:
            voices = self.tts_client.list_voices()
            
            languages = set()
            for voice in voices.voices:
                languages.update(voice.language_codes)
            
            return {
                "success": True,
                "languages": sorted(list(languages))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error getting languages: {str(e)}"
            }
    
    def process_audio_file(self, file_path: str, language: str = "en-US") -> Dict:
        """
        Process an audio file for speech recognition
        
        Args:
            file_path: Path to audio file
            language: Language code
            
        Returns:
            Dictionary with transcription result
        """
        try:
            # Read audio file
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Convert to speech
            return self.speech_to_text(audio_data, language)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing audio file: {str(e)}"
            }
    
    def save_audio_to_file(self, audio_data: str, file_path: str, format: str = "mp3") -> Dict:
        """
        Save base64 audio data to file
        
        Args:
            audio_data: Base64 encoded audio data
            file_path: Output file path
            format: Audio format
            
        Returns:
            Dictionary with result
        """
        try:
            # Decode audio data
            audio_bytes = base64.b64decode(audio_data)
            
            # Save to file
            with open(file_path, 'wb') as audio_file:
                audio_file.write(audio_bytes)
            
            return {
                "success": True,
                "file_path": file_path,
                "format": format
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error saving audio file: {str(e)}"
            }

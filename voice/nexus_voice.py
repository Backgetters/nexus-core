#!/usr/bin/env python3
"""
NEXUS Voice System
Free voice I/O using OpenAI Whisper (input) + macOS say (output)
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Configuration
VOICE_CONFIG = {
    "tts_voice": "Samantha",  # Female US voice
    "tts_fallback": "Karen",  # Female AU voice
    "whisper_model": "whisper-1",
    "temp_dir": Path.home() / ".nexus" / "voice_temp"
}

class VoiceSystem:
    """Voice I/O system for NEXUS"""
    
    def __init__(self):
        self.temp_dir = VOICE_CONFIG["temp_dir"]
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def speak(self, text: str, voice: str = None) -> bool:
        """
        Convert text to speech using macOS say command
        
        Args:
            text: Text to speak
            voice: Voice to use (default: Samantha)
        
        Returns:
            True if successful
        """
        if not voice:
            voice = VOICE_CONFIG["tts_voice"]
        
        try:
            # Use macOS say command
            subprocess.run(
                ["say", "-v", voice, text],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            # Try fallback voice
            if voice != VOICE_CONFIG["tts_fallback"]:
                return self.speak(text, VOICE_CONFIG["tts_fallback"])
            print(f"TTS Error: {e}")
            return False
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        Transcribe audio file using OpenAI Whisper
        
        Args:
            audio_path: Path to audio file
        
        Returns:
            Transcribed text
        """
        try:
            # Check if openai is available
            import openai
            
            # Get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "Error: OPENAI_API_KEY not set"
            
            client = openai.OpenAI(api_key=api_key)
            
            with open(audio_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model=VOICE_CONFIG["whisper_model"],
                    file=audio_file
                )
            
            return transcript.text
            
        except ImportError:
            return "Error: openai package not installed. Run: pip install openai"
        except Exception as e:
            return f"Transcription error: {str(e)}"
    
    def list_voices(self) -> list:
        """List available voices"""
        try:
            result = subprocess.run(
                ["say", "-v", "?"],
                capture_output=True,
                text=True
            )
            
            voices = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        voices.append({
                            'name': parts[0],
                            'lang': parts[1] if len(parts) > 1 else 'unknown'
                        })
            
            return voices
        except Exception as e:
            return [f"Error: {e}"]
    
    def test_voice(self):
        """Test voice system"""
        test_phrases = [
            "NEXUS voice system online.",
            "I can now speak responses.",
            "Voice test complete."
        ]
        
        print("🎙️ Testing voice system...")
        for phrase in test_phrases:
            print(f"   Speaking: {phrase}")
            self.speak(phrase)
        
        print("✅ Voice test complete")

# Quick test
if __name__ == "__main__":
    voice = VoiceSystem()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            voice.test_voice()
        elif sys.argv[1] == "speak":
            text = " ".join(sys.argv[2:])
            voice.speak(text)
        elif sys.argv[1] == "voices":
            voices = voice.list_voices()
            print("Available voices:")
            for v in voices[:20]:
                print(f"  {v}")
    else:
        # Default: test
        voice.test_voice()

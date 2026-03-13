#!/usr/bin/env python3
"""
NEXUS Voice Conversation Handler
Integrates with Telegram voice messages + desktop voice I/O
"""

import os
import sys
import tempfile
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from nexus_voice import VoiceSystem

class VoiceConversation:
    """Handle voice conversations"""
    
    def __init__(self):
        self.voice = VoiceSystem()
        self.conversation_log = Path(__file__).parent / "data" / "voice_log.jsonl"
        self.conversation_log.parent.mkdir(parents=True, exist_ok=True)
    
    def handle_voice_message(self, audio_path: str, source: str = "telegram") -> dict:
        """
        Handle incoming voice message
        
        Args:
            audio_path: Path to audio file (ogg from Telegram)
            source: Where message came from (telegram, desktop, etc.)
        
        Returns:
            dict with transcription and response
        """
        print(f"🎙️ Received voice from {source}")
        
        # Convert if needed (Telegram sends ogg, Whisper needs mp3/wav)
        converted_path = self._convert_audio(audio_path)
        
        # Transcribe
        transcription = self.voice.transcribe_audio(converted_path)
        print(f"   Heard: {transcription}")
        
        # Log
        self._log_interaction("received", transcription, source)
        
        return {
            "transcription": transcription,
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
    
    def respond_with_voice(self, text: str, speak: bool = True) -> dict:
        """
        Respond to user with text and optional voice
        
        Args:
            text: Response text
            speak: Whether to speak the response
        
        Returns:
            dict with response details
        """
        if speak:
            print(f"🔊 Speaking response...")
            success = self.voice.speak(text)
        else:
            success = False
        
        # Log
        self._log_interaction("sent", text, "voice" if speak else "text")
        
        return {
            "text": text,
            "spoken": success,
            "timestamp": datetime.now().isoformat()
        }
    
    def _convert_audio(self, audio_path: str) -> str:
        """Convert audio to format Whisper can handle"""
        # If already compatible format, return as-is
        if audio_path.endswith(('.mp3', '.wav', '.m4a', '.webm')):
            return audio_path
        
        # Convert ogg (Telegram) to mp3
        if audio_path.endswith('.ogg'):
            output_path = audio_path.replace('.ogg', '.mp3')
            try:
                import subprocess
                subprocess.run(
                    ['ffmpeg', '-i', audio_path, '-ar', '16000', '-ac', '1', output_path],
                    check=True,
                    capture_output=True
                )
                return output_path
            except:
                # If ffmpeg not available, return original and hope for best
                return audio_path
        
        return audio_path
    
    def _log_interaction(self, direction: str, content: str, source: str):
        """Log voice interaction"""
        import json
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "direction": direction,
            "content": content[:200],  # Truncate long content
            "source": source
        }
        
        with open(self.conversation_log, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def get_conversation_history(self, limit: int = 10) -> list:
        """Get recent conversation history"""
        if not self.conversation_log.exists():
            return []
        
        import json
        
        history = []
        with open(self.conversation_log) as f:
            for line in f:
                try:
                    history.append(json.loads(line))
                except:
                    continue
        
        return history[-limit:]

# Integration with OpenClaw
class VoiceHandler:
    """OpenClaw integration for voice"""
    
    def __init__(self):
        self.conversation = VoiceConversation()
    
    def on_voice_message(self, audio_file: str, chat_id: str) -> str:
        """
        Called when voice message received
        
        Returns text response (voice spoken separately)
        """
        # Transcribe
        result = self.conversation.handle_voice_message(audio_file, "telegram")
        user_text = result["transcription"]
        
        # Return transcription for processing by main agent
        return user_text
    
    def speak_response(self, text: str):
        """Speak response text"""
        self.conversation.respond_with_voice(text, speak=True)

if __name__ == "__main__":
    handler = VoiceHandler()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "speak":
            text = " ".join(sys.argv[2:])
            handler.speak_response(text)
        elif sys.argv[1] == "test":
            print("🎙️ Voice conversation system ready")
            print("   Voice: Samantha (female US)")
            print("   Transcription: OpenAI Whisper")
            print("   Status: Active")
            handler.speak_response("NEXUS voice system is now active. I can hear you and respond by voice.")
    else:
        print("Usage: python3 voice_conversation.py [speak <text>|test]")

# NEXUS Voice System
## Free Voice I/O Setup

---

## Components

| Component | Technology | Cost | Purpose |
|-----------|-----------|------|---------|
| **Text-to-Speech** | macOS `say` | Free | Speak responses |
| **Speech-to-Text** | OpenAI Whisper | API usage | Transcribe voice messages |
| **Voice** | Samantha (en_US) | Free | Female US voice |
| **Fallback** | Karen (en_AU) | Free | Female AU voice |

---

## Usage

### Desktop Voice
```bash
# Test voice system
cd ~/clawd/voice && python3 nexus_voice.py test

# Speak specific text
python3 nexus_voice.py speak "Hello, this is NEXUS"

# List available voices
python3 nexus_voice.py voices
```

### Telegram Voice Messages
1. Send voice message to bot
2. Bot transcribes using Whisper
3. Bot responds with text + voice (optional)

### Voice Conversation Mode
```bash
# Activate voice conversation
python3 voice_conversation.py test
```

---

## Configuration

### Environment Variables
```bash
# Required for Whisper transcription
export OPENAI_API_KEY="your-key-here"

# Optional: Default voice
export NEXUS_VOICE="Samantha"
```

### Available Female Voices
| Voice | Language | Quality |
|-------|----------|---------|
| Samantha | en_US | ⭐⭐⭐⭐⭐ |
| Karen | en_AU | ⭐⭐⭐⭐ |
| Moira | en_IE | ⭐⭐⭐⭐ |
| Tessa | en_ZA | ⭐⭐⭐⭐ |

---

## Files

| File | Purpose |
|------|---------|
| `nexus_voice.py` | Core TTS/STT functions |
| `voice_conversation.py` | Conversation handler |
| `data/voice_log.jsonl` | Conversation history |

---

## Integration with Main System

When voice message received:
1. Transcribe with Whisper
2. Process text through main NEXUS
3. Generate response
4. Speak response with `say`
5. Send text back to user

---

## Testing

```bash
# Quick test
cd ~/clawd/voice
python3 nexus_voice.py test

# Should hear:
# "NEXUS voice system online"
# "I can now speak responses"
# "Voice test complete"
```

---

## Notes

- **Free tier**: macOS say is completely free
- **Whisper cost**: ~$0.006 per minute of audio
- **Quality**: Good enough for notifications, not audiobook quality
- **Alternative**: ElevenLabs for premium quality (paid)

---

*Voice system active. Ready for voice conversations.*

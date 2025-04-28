import time
import pyttsx3
import os
from pathlib import Path
import re
import pygame

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from base import BotBase

class TTS:
    def __init__(self, bot: 'BotBase', cache_dir="tts/cache"):
        """Initialize TTS with caching support"""
        self.bot = bot
        self.engine = pyttsx3.init()
        self.cache_dir = Path(cache_dir)
        if not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Set default properties
        self.engine.setProperty('rate', 200)    # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Initialize pygame mixer
        if self.bot is None:
          pygame.mixer.init()
        
    def _get_cache_path(self, text):
        """Generate a cache file path using the text as filename"""
        # Sanitize the text to make it a valid filename
        # Replace invalid characters with underscores
        safe_text = re.sub(r'[<>:"/\\|?*]', '_', text)
        # Limit length to avoid issues with long filenames
        safe_text = safe_text[:100]
        return self.cache_dir / f"{safe_text}.wav"
        
    def speak(self, text, use_cache=True):
        """Speak the given text, using cache if available"""
        cache_path = self._get_cache_path(text)
        
        # If not in cache or cache disabled, generate and save new audio
        if not use_cache or not cache_path.exists():
            self.engine.save_to_file(text, str(cache_path))
            self.engine.runAndWait()  # Wait for file to be saved
        
        # Play the audio using pygame
        if self.bot is None:
            pygame.mixer.music.load(str(cache_path))
            pygame.mixer.music.play()
        else:
            self.bot.play_audio(cache_path, loops=1)
        
    def set_rate(self, rate):
        """Set the speech rate"""
        self.engine.setProperty('rate', rate)
        
    def set_volume(self, volume):
        """Set the volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', volume)
        
    def set_voice(self, voice_id):
        """Set the voice to use"""
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if voice.id == voice_id:
                self.engine.setProperty('voice', voice.id)
                break
                
def main():
    """Demonstrate TTS functionality"""
    # Initialize TTS
    tts = TTS(None)  # Pass None since we're not using the bot parameter
    
    # List available voices
    voices = tts.engine.getProperty('voices')
    print("Available voices:")
    for voice in voices:
        print(f"- {voice.id}")
    
    # Basic usage
    print("\nSpeaking with default settings...")
    tts.speak("Hello, this is a test of the text to speech system.")
    
    # Adjust rate
    print("\nSpeaking faster...")
    tts.set_rate(200)
    tts.speak("This is the same text spoken at a faster rate.")
    
    # Adjust volume
    print("\nSpeaking at lower volume...")
    tts.set_volume(0.5)
    tts.speak("This is the same text spoken at a lower volume.")
    
    # Test caching
    print("\nTesting cache (should be faster)...")
    tts.speak("This text should be cached and played from cache.")
    
    # Force new generation
    print("\nForcing new generation (not using cache)...")
    tts.speak("This text should be generated again.", use_cache=False)

    time.sleep(10)

if __name__ == "__main__":
    main()


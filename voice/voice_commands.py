import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import os
import threading
from fuzzywuzzy import process
import time
class VoiceCommand:
    def __init__(self, keyword_callbacks, model_path="models/vosk-model-small-en-us-0.15", min_similarity=40, delayBetweenWords=0.1):
    # def __init__(self, keyword_callbacks, model_path="models/vosk-model-en-us-0.22", min_similarity=75):
        """
        Initialize voice command listener
        :param keyword_callbacks: Dict of keyword -> callback function
        :param model_path: Path to vosk model
        :param min_similarity: Minimum similarity score (0-100) to accept a command match
        """
        self.delayBetweenWords = delayBetweenWords
        self.keyword_callbacks = keyword_callbacks
        self.model_path = model_path
        self.min_similarity = min_similarity
        self.q = queue.Queue()
        self.is_running = False
        self.thread = None
        self.enabled = True
        
        # Load model
        print(f"Loading model from: {model_path}")
        if not os.path.exists(model_path):
            print(f"Error: Model directory not found at {model_path}")
            print("Please download the model from https://alphacephei.com/vosk/models")
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)
        print("Model loaded successfully")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print("Audio error:", status)
        self.q.put(bytes(indata))

    def process_audio(self):
        while self.is_running:
            data = self.q.get()
            if self.rec.AcceptWaveform(data):
                result = json.loads(self.rec.Result())
                text = result.get("text", "").strip().lower()
                if not text:
                    continue
                    
                print(f"Full result: {text}")
                words = text.split()
                for word in words:
                    # Try exact match first
                    if word in self.keyword_callbacks:
                        # print(f">>> {word.upper()} detected — triggering callback")
                        self.keyword_callbacks[word]()
                        time.sleep(self.delayBetweenWords)
                        continue
                    
                    # Try fuzzy matching
                    match, score = process.extractOne(word, self.keyword_callbacks.keys())
                    print(f"Fuzzy match: '{word}' -> '{match}' (score: {score})")
                    
                    if score >= self.min_similarity:
                        # print(f">>> {match.upper()} detected via fuzzy match — triggering callback")
                        self.keyword_callbacks[match]()
                        time.sleep(self.delayBetweenWords)
            else:
                # Just ignore partial results - only use complete phrases
                pass

    def clear_queue(self):
        if not self.enabled:
            return
        if self.q is not None:
            with self.q.mutex:
                self.q.queue.clear()

    def start(self):
        """Start listening for voice commands in a separate thread"""
        if self.is_running or not self.enabled:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.start()
        print("Voice command listener started")

    def stop(self):
        """Stop listening for voice commands"""
        if not self.enabled:
            return
        self.is_running = False
        try:
            if self.thread:
                self.thread.join()
        except Exception as e:
            print(f"Error stopping voice command listener, might already stopped: {e}")
        print("Voice command listener stopped")

    def _run(self):
        """Internal method to run the audio stream"""
        try:
            with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                                 channels=1, callback=self.audio_callback):
                print("Say any command. Available commands:")
                for cmd in sorted(self.keyword_callbacks.keys()):
                    print(f"- {cmd}")
                print("Listening...")
                self.process_audio()
        except Exception as e:
            print(f"Error occurred: {e}")
            self.stop()

# Example usage:
if __name__ == "__main__":
    def on_left():
        print("Left command triggered!")
        
    def on_right():
        print("Right command triggered!")
        
    def on_up():
        print("Up command triggered!")
        
    def on_down():
        print("Down command triggered!")
        
    def on_done():
        print("Done command triggered!")
        
    def on_go():
        print("Go command triggered!")

    # Create callbacks dictionary
    callbacks = {
        "left": on_left,
        "right": on_right,
        "up": on_up,
        "down": on_down,
        "done": on_done,
        "go": on_go
    }

    # Create and start voice command listener
    voice_cmd = VoiceCommand(callbacks)
    try:
        voice_cmd.start()
        # Keep the main thread alive
        while True:
            pass
    except KeyboardInterrupt:
        voice_cmd.stop()

import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from base import BotBase

class BotVoiceConfig:
    def __init__(self, bot: 'BotBase'):
        self.bot = bot
        # We only need the core commands now since we're using fuzzy matching
        self.voice_commands = {
            "left": self.left,
            "right": self.right,
            "up": self.up,
            "down": self.down,

            "reset": self.reset,
            "go": self.go
        }

    def left(self):
        print("LEFT command received")
        self.bot.press_release('left')

    def right(self):
        print("RIGHT command received")
        self.bot.press_release('right')

    def up(self):
        print("UP command received")
        self.bot.press_release('up')

    def down(self):
        print("DOWN command received")
        self.bot.press_release('down')
        
    def reset(self):
        print("DONE command received")
        self.bot.rune_in_progress = False

    def go(self):
        print("GO command received")
        self.bot.press_release('y')

    def get_voice_commands(self):
        return self.voice_commands


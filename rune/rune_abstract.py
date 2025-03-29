from abc import abstractmethod, abstractproperty
from base import BotBase

class RuneWalkerPilot:
    def __init__(self):
        self.bot: BotBase = None  # Expect this to be set by subclasses

    @abstractmethod
    def rune_flash_jump(self):
        pass
    
    @abstractmethod
    def rune_jump(self):
        pass

    @abstractmethod
    def rune_rope(self):
        pass
    
    @abstractmethod
    def rune_jump_down(self):
        pass
    
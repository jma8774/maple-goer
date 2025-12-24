from abc import abstractmethod, abstractproperty
from base import BotBase

class RuneWalkerPilot:
    """
    Abstract base class for classes that can use RuneWalker functionality.
    Subclasses must implement all abstract methods to define character-specific
    movement and interaction for rune solving.
    """
    def __init__(self):
        self.bot: BotBase = None  # Expect this to be set by subclasses

    @abstractmethod
    def rune_flash_jump(self, direction=None):
        """
        Execute a flash jump or equivalent mobility skill.
        For Marksman: flash jump
        For Evan/Dragon: teleport
        """
        pass
    
    @abstractmethod
    def rune_jump(self):
        """
        Execute a basic jump.
        Usually just press 'w' or equivalent jump key.
        """
        pass

    @abstractmethod
    def rune_rope(self):
        """
        Climb up a rope or ladder.
        For Marksman: rope climbing
        For Evan/Dragon: teleport up
        """
        pass
    
    @abstractmethod
    def rune_jump_down(self):
        """
        Jump down through a platform.
        For Marksman: jump down
        For Evan/Dragon: teleport down
        """
        pass

    @abstractmethod
    def rune_protect(self):
        """
        Activate a protection skill before interacting with rune.
        For Marksman: solar crest or spider web
        For Evan/Dragon: spider web
        """
        pass
    
    @abstractmethod
    def rune_interact(self):
        """
        Interact with the rune (press interaction key).
        Usually 'space' or 'y' key.
        """
        pass
    
    

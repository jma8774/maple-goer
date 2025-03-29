from rune.rune_abstract import RuneWalkerPilot
from base import Audio, Images
import pyautogui as pag
import common
from state import state
import time
import math
class RuneWalker:
    def __init__(self, pilot: RuneWalkerPilot):
        self.pilot = pilot
        self.move_seq = 0

    def flash_jump(self):
        self.pilot.rune_flash_jump()

    def rope(self):
        self.pilot.rune_rope()

    def jump_down(self):
        self.pilot.rune_jump_down()

    def jump(self):
        self.pilot.rune_jump()

    def go(self, play_sound=True):
        rune_loc = self.find_rune()
        print(f"Rune: {rune_loc}")
    
        # Keep moving until the rune is found
        while state['running'] and rune_loc is not None:
            me_loc = self.find_me()
            rune_loc = self.find_rune()

            if me_loc is None or rune_loc is None:
                print("Failed to find me or rune, exiting")
                break
            print(f"Me: {me_loc}, Rune: {rune_loc}")

            vector = self.determine_vector_to_rune(me_loc, rune_loc)
            print(f"Vector: {vector}")
            self.make_a_move(vector)

        # Ping sound
        if play_sound:
            print("Pinging")
            self.pilot.bot.play_audio(Audio.PING, loops=2)
            time.sleep(2)
    ''' 
    Find the player's position
    Return (x, y)
    '''
    def find_me(self):
        try:
            return pag.locateOnScreen(Images.ME_PERSON, confidence=0.8, region=common.minimap_rune_region)
        except Exception as e:
            print(e)
            return None

    '''
    Find the rune's position
    Return (x, y)
    '''
    def find_rune(self):
        try:
            return pag.locateOnScreen(Images.RUNE_MINIMAP, confidence=0.8, region=common.minimap_rune_region)
        except Exception as e:
            print(e)
            return None

    '''
    Determine the vector to the rune
    Return (dx, dy)
    '''
    def determine_vector_to_rune(self, me_loc, rune_loc):
        dx = self.round_to_0_if_margin(rune_loc[0] - me_loc[0])
        dy = self.round_to_0_if_margin(rune_loc[1] - me_loc[1])
        return (dx, dy)
    
    '''
    Move to the rune
    '''
    def make_a_move(self, vector):
        self.move_seq += 1
        dx, dy = vector
        # Quick jump left or right in case we on rope every 3 moves 
        if dx > 0:
            self.pilot.bot.press('right')
            if self.move_seq % 3 == 0:
                self.jump()
                time.sleep(0.8)
            self.pilot.bot.release('right')
        elif dx < 0:
            self.pilot.bot.press('left')
            if self.move_seq % 3 == 0:
                self.jump()
                time.sleep(0.8)
            self.pilot.bot.release('left')

        # Flash jump if too far away
        if abs(dx) > 40:
            fj_times = math.ceil(abs(dx) / 40)
            print(f"Flash jump {fj_times} times")
            for _ in range(fj_times):
                self.flash_jump()
                time.sleep(0.15)
            return
        
        # Move left or right if closer
        x_seconds = abs(dx) / 20
        if dx > 0:
            self.pilot.bot.press_release('right', delayInBetween=x_seconds)
        elif dx < 0:
            self.pilot.bot.press_release('left', delayInBetween=x_seconds)
        
        # If rune is below, we need to jump down
        # If rune is above, we need to rope up
        if dy > 0:
            self.jump_down()
            time.sleep(0.5)
        elif dy < 0:
            self.rope()
            time.sleep(0.5)

    def round_to_0_if_margin(self, value, margin=5):
        if -margin <= value and value <= margin:
            return 0
        return value

    


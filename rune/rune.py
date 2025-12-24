from rune.rune_abstract import RuneWalkerPilot
from base import Audio, Images
import pyautogui as pag
import common
from state import state
import time
import math

def get_rune_buff_region():
    if state['fakefullscreen']:
        return (1060, 70, 1367-1060, 106-70)
    return (1060, 35, 1367-1060, 75-35)

class RuneWalker:
    def __init__(self, pilot: RuneWalkerPilot):
        self.pilot = pilot
        self.move_seq = 0


    def flash_jump(self, direction=None):
        self.pilot.rune_flash_jump(direction=direction)

    def rope(self):
        self.pilot.rune_rope()

    def jump_down(self):
        self.pilot.rune_jump_down()

    def jump(self):
        self.pilot.rune_jump()

    def go(self, play_sound=True):
        rune_loc = self.find_rune()
        try_left = True
        print(f"Rune: {rune_loc}")
    
        # Keep moving until the rune is found
        while state['running'] and rune_loc is not None:
            me_loc = self.find_me()
            rune_loc = self.find_rune()

            if me_loc is None:
                if try_left:
                    self.flash_jump(direction='left')
                    try_left = False
                else:
                    self.flash_jump(direction='right')
                    try_left = True
                time.sleep(0.5)
                continue
                    
            if rune_loc is None:
                print("Failed to find me or rune, exiting")
                break
            print(f"Me: {me_loc}, Rune: {rune_loc}")

            vector = self.determine_vector_to_rune(me_loc, rune_loc)
            print(f"Vector: {vector}")
            self.make_a_move(vector)

        # Ping sound
        self.pilot.bot.rune_in_progress = True
        ping_seq = 0
        self.pilot.rune_protect()
        while play_sound and self.pilot.bot.rune_in_progress:
            if ping_seq % 5 == 0:
                self.pilot.bot.play_audio(Audio.PING, loops=1)
                if ping_seq == 0:
                    # self.pilot.bot.voice_command.clear_queue()
                    # self.pilot.bot.voice_command.start()
                    self.pilot.rune_interact()
            ping_seq += 1
            time.sleep(1)
            if common.locate_center_on_screen(Images.RUNE_BUFF, confidence=0.7, region=get_rune_buff_region()):
                self.pilot.bot.rune_in_progress = False
        # self.pilot.bot.voice_command.stop()
    ''' 
    Find the player's position
    Return (x, y)
    '''
    def find_me(self):
        try:
            return common.locate_on_screen(Images.ME_PERSON, confidence=0.8, region=common.minimap_rune_region)
        except Exception as e:
            print(e)
            return None

    '''
    Find the rune's position
    Return (x, y)
    '''
    def find_rune(self):
        try:
            return common.locate_on_screen(Images.RUNE_MINIMAP, confidence=0.8, region=common.minimap_rune_region)
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
            direction = 'right' if dx > 0 else 'left'
            for _ in range(fj_times):
                self.flash_jump(direction=direction)
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

    


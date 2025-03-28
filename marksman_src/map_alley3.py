import time
import random
from datetime import datetime, timedelta
import pyautogui as pag
from base import Images
from state import state
from common import uniform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marksman import Marksman

def alley3_macro(marksman: 'Marksman'):
    """
    Alley 3 map farming macro for Marksman class
    """
    erda_counter = 0
    
    def alley3_rotation():
        nonlocal erda_counter
        cur = datetime.now()
        
        # Use erda fountain if available
        if cur > marksman.data['next_erda_fountain']:
            erda_counter += 1
            marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
            if False:
                marksman.jump_down_attack(delayAfter=0.47)
                marksman.erda_fountain()
                marksman.teleport_reset()
            else:
                marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
                marksman.jump_down_attack_turn(delayAfter=0.45, turn='left')
                marksman.bot.press('left', 0.7)
                marksman.bot.release('left')
                marksman.erda_fountain()
                marksman.jump_down_attack(delayAfter=0.48)
                marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
                marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.53)
                marksman.bot.press_release('right')
                marksman.teleport_reset()
                marksman.data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
                
        # Find mob before starting rotation
        if state['scanmob']:
            mob_loc = None
            count = 0
            interval = 0.1
            while mob_loc == None:
                mob_loc = pag.locateOnScreen(Images.ALLEY3_MOB, confidence=0.75, grayscale=True, region=marksman.alley3_region) or pag.locateOnScreen(Images.ALLEY3_MOB2, confidence=0.75, grayscale=True, region=marksman.alley3_region)
                time.sleep(interval)
                count += 1
                if count > (6/interval): break # 6 seconds
            if mob_loc == None:
                print(f"Couldn't find mob after {count} tries, continuing rotation")
            else:
                print(f"Found mob at {mob_loc}, continuing rotation")
                
        marksman.bot.press_release('e', 0.15)
        marksman.q_and_surgebolt(afterDelay=0.52)
        marksman.bot.press_release('left')
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.51)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.77)
        
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            marksman.jump_down_attack(delayAfter=0.45)
            marksman.bot.press_release('right')
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.51)
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.53)
            marksman.teleport_reset()
        else:
            marksman.jump_up(delayAfter=1)
            marksman.bot.press_release('right')
            marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
            marksman.teleport_reset()
    
    print("Started Alley 3 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        alley3_rotation()
    print("Paused Alley 3 macro")
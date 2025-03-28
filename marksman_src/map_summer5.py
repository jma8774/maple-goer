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

def summer5_macro(marksman: 'Marksman'):
    """
    Summer 5 map farming macro for Marksman class
    """
    erda_seq = 0
    
    def loot():
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            return
            
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.5)
        marksman.jump_down_attack_turn(delayAfter=0.5, turn='right')
        marksman.jump_down_attack(delayAfter=0.5)  
        marksman.jump_down_attack(delayAfter=0.5)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.5)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.5)
        marksman.jump_up(delayBetween=0.4, delayAfter=0.4)
        marksman.bolt_burst()
        marksman.shoot()
        marksman.bot.press_release('left')
        marksman.bot.press_release('left')
        marksman.teleport_reset()
        marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

    def rotation():
        nonlocal erda_seq
        
        # Find mob before starting rotation
        if state['scanmob']:
            mob_loc = None
            count = 0
            interval = 0.1
            while mob_loc == None:
                mob_loc = pag.locateOnScreen(Images.SUMMER5_MOB, confidence=0.95, grayscale=True, region=marksman.summer5_region) or pag.locateOnScreen(Images.SUMMER5_MOB2, confidence=0.95, grayscale=True, region=marksman.summer5_region)
                time.sleep(interval)
                count += 1
                if count > (6/interval): break # 6 seconds
            if mob_loc == None:
                print(f"Couldn't find mob after {count} tries, continuing rotation")
            else:
                print(f"Found mob at {mob_loc}, continuing rotation")

        marksman.jump_down_attack(attackDelay=0.3, delayAfter=0.35)
        marksman.bot.press_release('right')
        marksman.bot.press_release('right')
        marksman.shoot(delayAfter=0.53)
        marksman.jump_down_attack_turn(attackDelay=0.3, delayAfter=0.45, turn='left')
        marksman.bot.press_release('right')
        marksman.bot.press_release('right')
        
        if marksman.data['next_erda_fountain'] - timedelta(seconds=1) < datetime.now():
            marksman.jump_down(delayAfter=0.7)
            if erda_seq % 2 == 0:
                marksman.jump_down_attack(delayAfter=0.5)
                marksman.covering_fire(delayAfter=0.8)
            else:
                marksman.covering_fire()
                marksman.jump_down_attack(delayAfter=0.5)
            erda_seq += 1
            marksman.bot.press('right', delay=0.3)
            marksman.bot.release('right')
            marksman.erda_fountain()
            if not marksman.web():
                marksman.bolt_burst()
            marksman.bot.press_release('left')
            marksman.bot.press_release('left')
            marksman.teleport_reset()
        else:
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.5)
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.52)
            marksman.bot.press_release('left')
            marksman.bot.press_release('left')
            marksman.teleport_reset()
    
    print("Started Gentle Summer 5 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        rotation()
        loot()
    print("Paused Gentle Summer 5 macro")
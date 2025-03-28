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

def gate1_macro(marksman: 'Marksman'):
    """
    Road to the Castle's Gate 1 map farming macro for Marksman class
    """
    def gate1_rotation():
        just_erda = False
        cur = datetime.now()
        # Use erda fountain if available
        if cur > marksman.data['next_erda_fountain']:
            marksman.bot.press_release('shift', 0.8)
            marksman.erda_fountain()
            just_erda = True

        if just_erda:
            marksman.q_and_surgebolt(afterDelay=0.47)
            marksman.jump_down_attack_turn(delayAfter=0.45, turn='left')
            marksman.q_and_surgebolt(afterDelay=0.47)
            marksman.bot.press_release('right')
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.47)
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.47)
            marksman.teleport_reset()
        else:
            # Find mob before starting rotation
            if state['scanmob']:
                mob_loc = None
                count = 0
                interval = 0.15
                while mob_loc == None:
                    mob_loc = pag.locateOnScreen(Images.DIAMOND_GUARDIAN1, confidence=0.75, grayscale=True, region=marksman.gate1_region) or pag.locateOnScreen(Images.DIAMOND_GUARDIAN2, confidence=0.75, grayscale=True, region=marksman.gate1_region)
                    time.sleep(interval)
                    count += 1
                    if count > (6/interval): break # 6 seconds
                if mob_loc == None:
                    print(f"Couldn't find mob after {count} tries, continuing rotation")
                else:
                    print(f"Found mob at {mob_loc}, continuing rotation")
                    
            marksman.q_and_surgebolt(afterDelay=0.47)
            marksman.jump_down_attack_turn(delayAfter=0.41, turn='left')
            marksman.jump_down_attack(delayAfter=0.41)
            marksman.bot.press_release('right')
            marksman.jump_attack(attackDelay=0.05, delayAfter=0.47)
            if random.random() > 0.6:
                marksman.jump_attack(attackDelay=0.05, delayAfter=0.47)
            marksman.teleport_reset()
    
    def gate1_loot():
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            return
            
        marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
        marksman.jump_down_attack(delayAfter=0.47)
        marksman.q_and_surgebolt(afterDelay=0.45)
        marksman.bot.press_release('left')
        marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
        marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
        marksman.jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
        marksman.bot.press_release('c', 0.9)
        if not marksman.bolt_burst(0.6):
            if not marksman.web(delayAfter=0.6):
                marksman.q_and_surgebolt(afterDelay=0.6)
        marksman.bot.press_release('right')
        if marksman.should_exit(): return
        marksman.teleport_reset()
        marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
        
    print("Started Road to the Castle's Gate 1 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        gate1_rotation()
        gate1_loot()
    print("Paused Road to the Castle's Gate 1 macro")

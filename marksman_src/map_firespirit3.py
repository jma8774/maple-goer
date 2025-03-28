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

def firespirit3_macro(marksman: 'Marksman'):
    """
    Fire Spirit 3 map farming macro for Marksman class
    """
    def firespirit3_rotation():
        cur = datetime.now()
        # Find mob before starting rotation
        if state['scanmob']:
            mob_loc = None
            count = 0
            interval = 0.15
            while mob_loc == None:
                mob_loc = pag.locateOnScreen(Images.FIRE_SPIRIT, confidence=0.75, grayscale=True, region=marksman.firespirit_region) or pag.locateOnScreen(Images.FIRE_SPIRIT2, confidence=0.75, grayscale=True, region=marksman.firespirit_region)
                time.sleep(interval)
                count += 1
                if count > (6/interval): break # 6 seconds
            if mob_loc == None:
                print(f"Couldn't find mob after {count} tries, continuing rotation")
            else:
                print(f"Found mob at {mob_loc}, continuing rotation")
            
        marksman.jump_down_attack(delayAfter=0.39)
        marksman.shoot()
        marksman.jump_down_attack_turn(delayAfter=0.44, turn='right')
        marksman.jump_down_attack(attackDelay=0.3, delayAfter=0.4)
        marksman.bot.press_release('left')
        marksman.jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
        marksman.jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
        cur = datetime.now()
        if cur > marksman.data['next_erda_fountain']:
            marksman.jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.54)
            marksman.bot.press_release('c', 1)
            if not marksman.bolt_burst(0.7):
                time.sleep(0.7)
            marksman.bot.press_release('shift', 0.8)
            marksman.erda_fountain()
            if datetime.now() > marksman.data['next_loot_2']:
                time.sleep(0.4)
                marksman.data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
            marksman.teleport_reset()
        else:
            marksman.teleport_reset()
      
    def firespirit3_loot():
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            return
            
        marksman.jump_down_attack(delayAfter=0.7)
        marksman.jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.53)
        time.sleep(0.3)
        marksman.bot.press_release('right')
        marksman.teleport_reset()
        marksman.jump_down_attack(delayAfter=0.7)
        marksman.jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.52)
        marksman.jump_down_attack(delayAfter=0.7)
        marksman.jump_down_attack_turn(delayAfter=0.36, turn='left')
        marksman.jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
        marksman.jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
        marksman.jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
        marksman.bot.check_rune()
        marksman.teleport_reset()
        marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
    
    print("Started Fire Spirit 3 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        firespirit3_rotation()
        firespirit3_loot()
    print("Paused Fire Spirit 3 macro")

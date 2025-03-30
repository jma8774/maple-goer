import time
import random
from datetime import datetime, timedelta
import pyautogui as pag
from base import Images
from state import state
import common
from common import uniform, locate_on_screen
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from marksman import Marksman

def bottomdeck6_macro(marksman: 'Marksman'):
    """
    Bottom Deck Passage 6 map farming macro for Marksman class
    """
    just_erda = False

    def rotation():
        nonlocal just_erda
        if not just_erda:
            # Find mob before starting rotation
            if state['scanmob']:
                mob_loc = None
                count = 0
                interval = 0.1
                while mob_loc == None:
                    mob_loc = common.locate_on_screen(Images.FLORA_SWORD1, confidence=0.95, grayscale=True, region=marksman.bottompassage6_region) or common.locate_on_screen(Images.FLORA_SWORD2, confidence=0.95, grayscale=True, region=marksman.bottompassage6_region)
                    time.sleep(interval)
                    count += 1
                    if count > (6/interval): break # 6 seconds
                if mob_loc == None:
                    print(f"Couldn't find mob after {count} tries, continuing rotation")
                else:
                    print(f"Found mob at {mob_loc}, continuing rotation")
            marksman.jump_attack_still(attackDelay=0.1, delayAfter=0.48)
        
        marksman.jump_down_attack_turn(delayAfter=0.48, turn='right')
        marksman.jump_down_attack(attackDelay=0.4, delayAfter=0.4)
        marksman.bot.press_release('left')
        marksman.bot.press_release('left')

        if datetime.now() < marksman.data['next_erda_fountain']:
            just_erda = False
            marksman.shoot()
            marksman.teleport_reset()
        else:
            just_erda = True
            fountain()
            rotation()

    def fountain():
        nonlocal just_erda
        if datetime.now() < marksman.data['next_erda_fountain']:
            return
        
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.52)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.52)
        marksman.bot.press('left', delay=0.07)
        marksman.bot.release('left')
        marksman.erda_fountain(custom_cd=56)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.51)
        marksman.rope(delayAfter=1.5)
        marksman.janus()
        marksman.bot.press_release('right')
        marksman.bot.press_release('right')
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.51)
        marksman.bot.press('right', delay=1)
        marksman.bot.release('right')
        marksman.janus2()
        marksman.bot.press_release('left')
        time.sleep(0.2)
        marksman.teleport_reset()
    
    def loot():
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            return
            
        marksman.shoot()
        marksman.bot.press_release('right')
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.53)
        marksman.jump_attack(attackDelay=0.05, delayAfter=1.2)
        marksman.bot.press_release('left')
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.50)
        marksman.jump_attack(attackDelay=0.05, delayAfter=0.50)
        marksman.teleport_reset()
        marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1, 1.2))
    
    print("Started Bottom Deck Passage 6 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        marksman.consumables_check()
        loot()
        rotation()
    print("Paused Bottom Deck Passage 6 macro")
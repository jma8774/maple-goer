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
    from mail import Marksman

def calm_beach_3_macro(marksman: 'Marksman'):
    marksman.data['_last_reset_in_place'] = datetime.now()
    marksman.data['_last_spawn'] = datetime.now() - timedelta(seconds=10)
    def rotation():
        # Find mob before starting rotation
        if state['scanmob']:
            mob_loc = None
            count = 0
            interval = 0.1
            while mob_loc == None:
                now = datetime.now()
                if now - marksman.data['_last_spawn'] < timedelta(seconds=6):
                    time.sleep(0.5)
                mob_loc = common.locate_on_screen(Images.ABYSSAL_GUARD_1, confidence=0.95, grayscale=True, region=marksman.bottompassage6_region) or common.locate_on_screen(Images.ABYSSAL_GUARD_2, confidence=0.95, grayscale=True, region=marksman.bottompassage6_region)
                time.sleep(interval)
                count += 1
                if count > (6/interval): break # 6 seconds
            if mob_loc == None:
                print(f"Couldn't find mob after {count} tries, continuing rotation")
            else:
                print(f"Found mob at {mob_loc}, continuing rotation")
        marksman.data['_last_spawn'] = datetime.now()
        marksman.shoot(delayAfter=0.575)
        marksman.bolt_burst()
        # if datetime.now() > marksman.data['_last_reset_in_place'] + timedelta(seconds=uniform(15, 30)):
        #     marksman.bot.press_release('left')
        #     marksman.teleport_reset()
        #     marksman.data['_last_reset_in_place'] = datetime.now()
        time.sleep(0.5)
    
    def setup_stationaries():
        marksman.bot.press_release('left')
        # TODO: jump here sometimes?
        marksman.rope(delayAfter=1.8)
        marksman.jump_attack(delayAfter=0.64)
        marksman.bot.press('left', 0.45)
        marksman.bot.release('left')
        marksman.janus()
        marksman.bot.press('left', 0.5)
        marksman.bot.release('left')
        marksman.jump_down_attack(delayAfter=0.68)
        marksman.jump_attack(delayAfter=0.68)
        marksman.janus2()
        marksman.jump_attack(delayAfter=0.67)
        marksman.janus3()
        marksman.flash_jump(jumpDelay=0.05, delayAfter=1.2, extraPress=True)
        marksman.erda_fountain(custom_cd=56)
        time.sleep(0.3) # To loot
        marksman.teleport_reset()
    
    def loot():
        if datetime.now() < marksman.data.get('next_loot', datetime.now()):
            return
          
        marksman.bot.press_release('left')
        marksman.flash_jump(delayAfter=0.6)
        marksman.bot.press('left', delay=1.3)
        marksman.bot.release('left')
        marksman.jump_attack(delayAfter=0.63)
        marksman.flash_jump(delayAfter=0.6)
        if uniform(0, 1) < 0.5:
            marksman.flash_jump(delayAfter=0.6)
        time.sleep(0.2)
        marksman.teleport_reset()
        marksman.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1, 1.2))
    
    print("Started Calm Beach 3 macro")
    while not marksman.should_exit():
        marksman.buff_setup()
        marksman.consumables_check()
        rotation()
        if datetime.now() > marksman.data['next_erda_fountain']:
          setup_stationaries()
        elif datetime.now() > marksman.data.get('next_loot', datetime.now()):
          loot()
    print("Paused Calm Beach 3 macro")
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
    from ricky2 import Ricky

def castle_gate_1_macro(evan: 'Ricky'):
    evan.data['_last_spawn'] = datetime.now() - timedelta(seconds=10)
    def rotation():
        # Find mob before starting rotation
        # if state['scanmob']:
        #     mob_loc = None
        #     count = 0
        #     interval = 0.1
        #     while mob_loc == None:
        #         now = datetime.now()
        #         if now - evan.data['_last_spawn'] < timedelta(seconds=6):
        #             time.sleep(0.5)
        #         mob_loc = common.locate_on_screen(Images.ABYSSAL_GUARD_1, confidence=0.95, grayscale=True, region=evan.monster_region) or common.locate_on_screen(Images.ABYSSAL_GUARD_2, confidence=0.95, grayscale=True, region=evan.monster_region)
        #         time.sleep(interval)
        #         count += 1
        #         if count > (6/interval): break # 6 seconds
        #     if mob_loc == None:
        #         print(f"Couldn't find mob after {count} tries, continuing rotation")
        #     else:
        #         print(f"Found mob at {mob_loc}, continuing rotation")
        # evan.data['_last_spawn'] = datetime.now()
        if not evan.data.get('dragon_finished_action', datetime.now()) < datetime.now():
            return
        if not evan.fire_breath():
            evan.wind_breath()
        time.sleep(0.5)
    
    def setup_stationaries():
        evan.teleport_right()
        evan.teleport_left(should_z=True)
        evan.teleport_up(should_z=True)
        evan.teleport_left(should_z=True)
        evan.teleport_left(should_z=True)
        evan.teleport_left(should_z=True)
        evan.erda_fountain()
        evan.teleport_left(should_z=True)
        evan.teleport_left(should_z=True)
        evan.bot.press('left', 0.6)
        evan.bot.release('left')
        evan.janus()
        evan.teleport_down()
        evan.teleport_right(should_z=True)
        evan.teleport_right(should_z=True)
        evan.teleport_right(should_z=True)
        evan.teleport_right(should_z=True)
        evan.teleport_right(should_z=True)
        evan.teleport_right(should_z=True)
        evan.teleport_right()
        evan.bot.press('left', 0.4)
        evan.bot.release('left')

    def loot():
        if datetime.now() < evan.data.get('next_loot', datetime.now()):
            return
          
        evan.data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1, 1.2))
    
    print("Started Castle Gate 1 macro")
    while not evan.should_exit():
        evan.buff_setup()
        evan.consumables_check()
        rotation()
        if datetime.now() > evan.data['next_erda_fountain']:
            setup_stationaries()
        elif datetime.now() > evan.data.get('next_loot', datetime.now()):
            loot()
    print("Paused Castle Gate 1 macro")

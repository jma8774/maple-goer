import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state
import common
from common import uniform, sleep
from rune.rune_abstract import RuneWalkerPilot
from rune.rune import RuneWalker
from database.database import Database
import interception
from evan_src.map_castle_gate_1 import castle_gate_1_macro


class Ricky(RuneWalkerPilot):
    # Region definitions
    monster_region = (550, 20, 810, 290)
    minimap_map_icon_region = (5, 15, 40, 40)
    confirmation_dialog_region = (550, 310, 815-550, 477-310)

    def __init__(self):
        self.bot = None
        self.database = Database(db_path="data/ricky_evan.json")
        self.data = {
            'dragon_finished_action': datetime.now(),
            'next_fire_floor': datetime.now(),
            'next_erda_fountain': self.database.get('next_erda_fountain', datetime.now()),
            'next_fire_breath': datetime.now(),
            'next_wind_breath': datetime.now(),
            'next_dark_fog': datetime.now(),
            'next_onyx_dragon': datetime.now(),
            'next_web': datetime.now(),
            'next_janus': self.database.get('next_janus', datetime.now()),
            'next_janus2': self.database.get('next_janus2', datetime.now()),
            'next_janus3': self.database.get('next_janus3', datetime.now()),
            'next_boss_buff': datetime.now() + timedelta(minutes=0.5),
            'next_familiar_fuel': datetime.now() + timedelta(hours=1),
            'next_loot': datetime.now() + timedelta(minutes=1.7),
            'whiteroomed': False,
            'is_paused': False
        }
        # Initialize script mapping
        self.scripts = {
            "gate1": lambda: castle_gate_1_macro(self),
            "default": lambda: castle_gate_1_macro(self)
        }

    def getMap(self):
        maps = {
            "gate1": Images.ODIUM_ICON,
            "default": Images.ODIUM_ICON
        }
        return maps[state['script']] if state['script'] in maps else maps['default']

    def main(self):
        config = {
            "user": "ricky",
            "script": self.scripts[state['script']],
            "setup": self.setup
        }
        self.consumable_setup()
        self.rune_walker = RuneWalker(self)
        self.bot = BotBase(self.data, config, args=sys.argv, scripts=self.scripts, runewalker=self.rune_walker)
        self.bot.run()

    def setup(self):
        self.data['next_petfood'] = datetime.now() + timedelta(seconds=90)

    def consumable_setup(self):
        self.data['bonus_exp_cp'] = self.database.get('bonus_exp_cp', datetime.min)
        self.data['regular_exp_cp'] = self.database.get('regular_exp_cp', datetime.min)
        self.data['legion_drop'] = self.database.get('legion_drop', datetime.min)
        self.data['legion_meso'] = self.database.get('legion_meso', datetime.min)
        self.data['wap'] = self.database.get('wap', datetime.min)
        self.data['eap'] = self.database.get('eap', datetime.min)

    def should_exit(self, func=None):
        # If used as a function call without arguments
        if func is None:
            if state['checkmap'] and not self.data.get('whiteroomed', False) and common.pause_if_whiteroom(pag, self.data, self.getMap()):
                self.data['whiteroomed'] = True
            if self.data.get('is_paused', False):
                raise Exception("Stopping thread")
            return False
            
        # If used as a decorator
        def wrapper(*args, **kwargs):
            if state['checkmap'] and not self.data.get('whiteroomed', False) and common.pause_if_whiteroom(pag, self.data, self.getMap()):
                self.data['whiteroomed'] = True
            if self.data.get('is_paused', False):
                raise Exception("Stopping thread")
            if callable(func):
                return func(self, *args, **kwargs)
                
        return wrapper

    def buff_setup(self):
        if self.should_exit(): return
        # if self.bot.check_rune_and_walk():
            # return

    def consumables_check(self):
        pass

    # Helper functions from original ricky.py
    def dark_fog(self, delayAfter=0.7):
        if self.should_exit(): return
        if datetime.now() < self.data['next_dark_fog']:
            return
        self.bot.press_release('pagedown', delayAfter)
        self.data['next_dark_fog'] = datetime.now() + timedelta(seconds=uniform(40, 50))
    
    def fire_breath(self):
        if self.should_exit(): return False
        if datetime.now() > self.data['next_fire_breath']:
            if datetime.now() < self.data['dragon_finished_action']:
                self.bot.press_release('ctrl')
            self.bot.press_release('g', delay=0.3)
            self.bot.press_release('t', delay=0.7)
            self.data['next_fire_breath'] = datetime.now() + timedelta(seconds=10)
            self.data['dragon_finished_action'] = datetime.now() + timedelta(seconds=5)
            return True
        return False
    
    def wind_breath(self):
        if self.should_exit(): return False
        if datetime.now() > self.data['next_wind_breath']:
            if datetime.now() < self.data['dragon_finished_action']:
                self.data['next_fire_breath'] = datetime.now()
                self.bot.press_release('ctrl')
            self.bot.press_release('a', delay=0.3)
            self.bot.press_release('f', delay=0.7)
            self.data['next_wind_breath'] = datetime.now() + timedelta(seconds=8)
            self.data['dragon_finished_action'] = datetime.now() + timedelta(seconds=5)
            return True
        return False

    def summon_onyx(self):
        if self.should_exit(): return False
        if datetime.now() > self.data['next_onyx_dragon']:
            self.bot.press_release('4')
            self.bot.press_release('4', 0.8)
            self.data['next_onyx_dragon'] = datetime.now() + timedelta(seconds=80)
            return True
        return False

    def summon_web(self, delayAfter=0.8):
        if self.should_exit(): return False
        if datetime.now() > self.data['next_web']:
            self.bot.press_release('delete', delayAfter)
            self.data['next_web'] = datetime.now() + timedelta(seconds=250)
            return True
        return False

    def erda_fountain(self):
        if self.should_exit(): return
        if datetime.now() > self.data['next_erda_fountain']:
            self.bot.press_release('x')
            self.data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_erda_fountain', self.data['next_erda_fountain'])

    def janus(self, delayAfter=0.75):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus']:
            self.bot.press_release('4')
            self.data['next_janus'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus', self.data['next_janus'])
            sleep(delayAfter)
            return True
        return False

    def janus2(self, delayAfter=0.75):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus2']:
            self.bot.press_release('4')
            self.data['next_janus2'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus2', self.data['next_janus2'])
            sleep(delayAfter)
            return True
        return False
    
    def janus3(self, delayAfter=0.75):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus3']:
            self.bot.press_release('4')
            self.data['next_janus3'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus3', self.data['next_janus3'])
            sleep(delayAfter)
            return True
        return False

    def teleport_up(self, delayAfter=0.45, should_z=False, z_delay_before_attack=0.15):
        if self.should_exit(): return
        self.bot.press('up')
        self.bot.press_release('d')
        if should_z:
            self.bot.release('up', delay=z_delay_before_attack)
            self.bot.press_release('z')
        else:
            self.bot.release('up')
        sleep(delayAfter, randomize_percentage=0.1)

    def teleport_down(self, delayAfter=0.45, should_z=False, z_delay_before_attack=0.15):
        if self.should_exit(): return
        self.bot.press('down')
        self.bot.press_release('d')
        if should_z:
            self.bot.release('down', delay=z_delay_before_attack)
            self.bot.press_release('z')
        else:
            self.bot.release('down')
        sleep(delayAfter, randomize_percentage=0.1)

    def teleport_left(self, delayAfter=0.45, should_z=False, z_delay_before_attack=0.15):
        if self.should_exit(): return
        self.bot.press('left')
        self.bot.press_release('d')
        if should_z:
            self.bot.release('left', delay=z_delay_before_attack)
            self.bot.press_release('z')
        else:
            self.bot.release('left')
        sleep(delayAfter, randomize_percentage=0.1)

    def teleport_right(self, delayAfter=0.45, should_z=False, z_delay_before_attack=0.15):
        if self.should_exit(): return
        self.bot.press('right')
        self.bot.press_release('d')
        if should_z:
            self.bot.release('right', delay=z_delay_before_attack)
            self.bot.press_release('z')
        else:
            self.bot.release('right')
        sleep(delayAfter, randomize_percentage=0.1)


# OVERRIDES FOR RUNE BOT INTERFACE
    def rune_flash_jump(self, direction=None):
        if direction == 'left':
            self.teleport_left()
        elif direction == 'right':
            self.teleport_right()

    def rune_rope(self):
        self.teleport_up()
    
    def rune_jump_down(self):
        self.teleport_down()

    def rune_jump(self):
        self.bot.press_release('w')

    def rune_protect(self):
        self.summon_web()
        sleep(0.3)
    
    def rune_interact(self):
        self.bot.press_release('space')
# END OF OVERRIDES FOR RUNE BOT INTERFACE


if __name__=="__main__":
    try:
        ricky = Ricky()
        ricky.main()
    except KeyboardInterrupt:
        state['running'] = False
        exit()

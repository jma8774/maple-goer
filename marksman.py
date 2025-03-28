import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state
import common
from common import uniform
from marksman_src.map_outlaw2 import outlaw2_macro
from marksman_src.map_alley3 import alley3_macro
from marksman_src.map_summer5 import summer5_macro
from marksman_src.map_bottomdeck6 import bottomdeck6_macro
from marksman_src.map_gate1 import gate1_macro
from marksman_src.map_firespirit3 import firespirit3_macro

class Marksman:
    # Region definitions
    ascendion_region = (0, 200, 450, 500)
    firespirit_region = (0, 450, 700, 750-450)
    ebon_region = (750, 230, 1365-750, 415-230)
    gate1_region = (5, 300, 365-5, 545-300)
    alley3_region = (0, 310, 670, 725-310)
    summer5_region = (2, 408, 772-2, 652-408)
    bottompassage6_region = (10, 165, 608-10, 513-165)

    def __init__(self):
        self.bot = None
        self.data = {
            'x_and_down_x': False,
            'next_sharpeye': datetime.now(),
            'next_split': datetime.now(),
            'next_blink_setup': None,
            'next_bird': datetime.now(),
            'next_pot': datetime.now() + timedelta(minutes=0.5),
            'next_boss_buff': datetime.now() + timedelta(minutes=0.5),
            'next_surgebolt': datetime.now(),
            'next_web': datetime.now(),
            'next_high_speed': datetime.now(),
            'next_bolt_burst': datetime.now(),
            'next_erda_fountain': datetime.now(),
            'next_janus': datetime.now(),
            'next_janus2': datetime.now(),
            'next_loot_2': datetime.now() + timedelta(minutes=1.5),
            'whiteroomed': False,
            'is_paused': False
        }
        # Initialize script mapping
        self.scripts = {
            "arcus": lambda: outlaw2_macro(self),
            "odium": lambda: alley3_macro(self),
            "shangrila": lambda: summer5_macro(self),
            "arteria": lambda: bottomdeck6_macro(self),
            "default": lambda: bottomdeck6_macro(self)
            # Commented out scripts
            # "cernium": lambda: firespirit3_macro(self),
            # "gate1": lambda: gate1_macro(self),
            # "burnium": self.ebonmage_macro,
        }

    def getMap(self):
        maps = {
            # "cernium": Images.CERNIUM_ICON,
            # "burnium": Images.BURNIUM_ICON,
            # "gate1": Images.ODIUM_ICON,
            "arcus": Images.ARCUS_ICON,
            "odium": Images.ODIUM_ICON,
            "shangrila": Images.SHANGRILA_ICON,
            "arteria": Images.ARTERIA_ICON,
            "default": Images.ARTERIA_ICON
        }
        return maps[state['script']] if state['script'] in maps else maps['default']

    def main(self):
        config = {
            "user": "jeemong",
            "script": self.scripts[state['script']],
            "setup": self.setup,
        }
        self.bot = BotBase(self.data, config, args=sys.argv, scripts=self.scripts)
        self.bot.run()

    def setup(self):
        self.data['x_and_down_x'] = True
        self.data['next_blink_setup'] = None
        self.data['next_split'] = datetime.now()
        self.data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(180, 220))
        self.data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 140))
        self.data['next_petfood'] = datetime.now() + timedelta(seconds=90)

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
        cur = datetime.now()
        
        self.bot.check_person_entered_map(only_guild=True)
        self.bot.check_fam_leveling()
        self.bot.check_tof("y")
        self.bot.check_wap()
        self.bot.check_fam_fuel()
        self.bot.check_elite_box()
        self.bot.check_rune()

        # if cur > self.data['next_petfood']:
        #   self.bot.press_release('f10')
        #   self.data['next_petfood'] = cur + timedelta(seconds=90)

        if cur > self.data['next_boss_buff'] and pag.locateOnScreen(Images.ELITE_BOSS_HP, region=(200, 0, 1150-200, 30)):
            self.bot.press_release('t', 0.5)
            self.bot.press_release('pageup', 0.45)
            self.bot.press_release('home', 0.45)
            self.bot.press_release('insert', 0.9)
            self.bot.press_release('delete', 0.6)
            self.web(delayAfter=0.4)
            self.data['next_boss_buff'] = cur + timedelta(minutes=uniform(1.5, 1.7))

        if self.data['x_and_down_x']:
            self.teleport_reset()
            self.bot.press('down')
            self.bot.press_release('x')
            self.bot.press_release('x')
            self.bot.release('down', 0.6)
            self.data['x_and_down_x'] = False
            self.data['next_blink_setup'] = cur + timedelta(seconds=uniform(54, 58))
            return

        if self.data['next_blink_setup'] == None:
            self.teleport_reset()
            self.data['next_blink_setup'] = cur + timedelta(seconds=uniform(54, 58))
            return
        elif cur > self.data['next_blink_setup']:
            self.bot.press('down')
            self.bot.press_release('x')
            self.bot.press_release('x')
            self.bot.release('down', 0.6)
                                                                            
    def shoot(self, delayAfter=0.51):
        if self.should_exit(): return
        self.bot.press_release('q', delay=delayAfter)

    def covering_fire(self, delayAfter=0.7):
        if self.should_exit(): return
        self.bot.press_release('shift', delay=delayAfter)

    def erda_fountain(self, delayAfter=0.5, custom_cd=59):
        if self.should_exit(): return
        if datetime.now() > self.data['next_erda_fountain']:
            self.bot.press_release('b')
            self.bot.press_release('b')
            self.data['next_erda_fountain'] = datetime.now() + timedelta(seconds=custom_cd)
            time.sleep(delayAfter)
            return True
        return False

    def janus(self, delayAfter=0.65):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus'] = datetime.now() + timedelta(seconds=59)
            time.sleep(delayAfter)
            return True
        return False

    def janus2(self, delayAfter=0.65):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus2']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus2'] = datetime.now() + timedelta(seconds=59)
            time.sleep(delayAfter)
            return True
        return False

    def bolt_burst(self, delayAfter=0.5, isGo=True):
        if self.should_exit(): return
        if isGo and datetime.now() > self.data['next_bolt_burst']:
            self.bot.press_release('d', delay=delayAfter)
            self.data['next_bolt_burst'] = datetime.now() + timedelta(seconds=7)
            return True
        return False

    def jump_web(self, jumpDelay=0.2, delayAfter=0.3):
        if self.should_exit(): return
        if datetime.now() > self.data['next_web']:
            self.jump_down(delayAfter=jumpDelay)
            self.web(delayAfter=delayAfter)
            return True
        return False

    def web(self, delayAfter=0.3):
        if self.should_exit(): return
        if datetime.now() > self.data['next_web']:
            self.bot.press_release('4', delay=delayAfter)
            self.data['next_web'] = datetime.now() + timedelta(seconds=251)
            return True
        return False

    def jump_high_speed_shot(self, jumpDelay=0.2, delayAfter=0.3, isGo=True):
        if self.should_exit(): return
        if isGo and datetime.now() > self.data['next_high_speed']:
            self.jump_down(delayAfter=jumpDelay)
            self.high_speed_shot(delayAfter=delayAfter)
            return True
        return False

    def high_speed_shot(self, delayAfter=0.3, isGo=True):
        if self.should_exit(): return
        if isGo and datetime.now() > self.data['next_high_speed']:
            self.bot.press_release('a', delay=delayAfter)
            self.data['next_high_speed'] = datetime.now() + timedelta(seconds=15)
            return True
        return False

    def flash_jump(self, jumpDelay=0.2, delayAfter=0.7):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('e', delayAfter)

    def jump_attack(self, attackDelay=0.2, jumpDelay=0.05, delayAfter=0.52, withSurge=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('e', attackDelay)
        self.bot.press_release('q')
        if withSurge:
            self.surgebolt()
        time.sleep(delayAfter)

    def jump_attack_still(self, attackDelay=0.05, delayAfter=0.65):
        if self.should_exit(): return
        self.bot.press_release('e', attackDelay)
        self.bot.press_release('q')
        time.sleep(delayAfter)

    def jump_up(self, delayBetween=0.2, delayAfter=1):
        if self.should_exit(): return
        self.bot.press('up')
        self.bot.press_release('e', delayBetween)
        self.bot.press_release('e')
        self.bot.press_release('e')
        self.bot.release('up', delayAfter)

    def jump_down(self, delayAfter=1):
        if self.should_exit(): return
        self.bot.press('down', 0.15)
        self.bot.press('e', 0.15)
        self.bot.release('e')
        self.bot.release('down', delayAfter)

    def jump_down_attack(self, attackDelay=0.05, delayAfter=1):
        if self.should_exit(): return
        self.bot.press('down')
        self.bot.press('e', attackDelay)
        self.bot.press_release('q')
        self.bot.release('e')
        self.bot.release('down', delayAfter)

    def jump_down_attack_turn(self, attackDelay=0.05, delayAfter=1, turn='left'):
        if self.should_exit(): return
        self.bot.press('down', delay=0.04)
        self.bot.press('e', delay=0.04)
        if turn == 'left':
            self.bot.press_release('left', delay=0.02)
        else:
            self.bot.press_release('right', delay=0.02)
        time.sleep(attackDelay)
        self.bot.press_release('q', delay=0.02)
        self.bot.release('e', delay=0.02)
        self.bot.release('down', delayAfter)

    def jump_down_and_fj(self, delayAfter=1):
        if self.should_exit(): return
        self.jump_down(delayAfter=uniform(0.3, 0.5))
        self.bot.press('e')
        self.bot.release('e')
        self.bot.press('e')
        self.bot.release('e', delayAfter)

    def surgebolt(self, delayAfter=0.05):
        if datetime.now() > self.data['next_surgebolt']:
            self.bot.press_release('r')
            self.data['next_surgebolt'] = datetime.now() + timedelta(seconds=10)
            time.sleep(delayAfter)
            return True
        return False

    def q_and_surgebolt(self, afterDelay=0.7):
        if self.should_exit(): return
        if datetime.now() > self.data['next_surgebolt']:
            self.bot.press('q', delay=0.02)
            self.bot.press_release('r')
            self.bot.release('q', afterDelay)
            self.data['next_surgebolt'] = datetime.now() + timedelta(seconds=uniform(10, 13))
        else:
            self.bot.press_release('q', afterDelay)

    def rope(self, delayAfter=2):
        if self.should_exit(): return
        self.bot.press_release('c', delayAfter)

    def teleport_reset(self, delayAfter=0.65):
        if self.should_exit(): return
        self.bot.press_release('x')
        self.bot.press_release('x', delayAfter)

if __name__=="__main__":
    marksman = Marksman()
    marksman.main()

  
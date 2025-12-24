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


class Ren(RuneWalkerPilot):
    # Region definitions

    confirmation_dialog_region = (550, 310, 815-550, 477-310)

    def __init__(self):
        self.bot = None
        self.database = Database(db_path="data/jeemong_ren.json")
        self.data = {
            'next_buff_check': datetime.now() + timedelta(seconds=15),
            'next_decents': datetime.now() + timedelta(seconds=181),
            'next_erda_fountain': self.database.get('next_erda_fountain', datetime.now()),
            'next_janus': self.database.get('next_janus', datetime.now()),
            'next_janus2': self.database.get('next_janus2', datetime.now()),
            'next_janus3': self.database.get('next_janus3', datetime.now()),
            'next_familiar_fuel': datetime.now() + timedelta(hours=1),
            'whiteroomed': False,
            'is_paused': False,
            'consumable_enabled': "enabled",
            'use_inventory_region': None
        }
        # Initialize script mapping - TODO: Add Ren-specific map macros
        self.scripts = {
            "default": lambda: self.default_macro()
        }

    def getMap(self):
        maps = {
            "arcus": Images.ARCUS_ICON,
            "odium": Images.ODIUM_ICON,
            "shangrila": Images.SHANGRILA_ICON,
            "arteria": Images.ARTERIA_ICON,
            "carcion": Images.CARCION_ICON,
            "default": Images.CARCION_ICON
        }
        return maps[state['script']] if state['script'] in maps else maps['default']

    def main(self):
        config = {
            "user": "jeemong",
            "script": self.scripts[state['script']],
            "setup": self.setup
        }
        self.consumable_setup()
        self.rune_walker = RuneWalker(self)
        self.bot = BotBase(self.data, config, args=sys.argv, scripts=self.scripts, runewalker=self.rune_walker)
        self.bot.run()

    def setup(self):
        pass

    def consumable_setup(self):
        self.data['bonus_exp_cp'] = self.database.get('bonus_exp_cp', datetime.min)
        self.data['regular_exp_cp'] = self.database.get('regular_exp_cp', datetime.min) # This include Legion
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
        if self.bot.check_rune_and_walk():
            return
        cur = datetime.now()
        
        # self.bot.check_person_entered_map(only_guild=True)
        self.bot.check_elite_box()

        if cur > self.data['next_decents']:
            self.bot.press_release('pagedown', 1.5)
            # Pet Food
            self.bot.press_release('f10', 0.5)
            self.bot.press_release('f10', 0.5)
            self.data['next_decents'] = cur + timedelta(seconds=181)

    def consumables_check(self):
        if self.data['consumable_enabled'] == "disabled": return
        print(f"Consumable setup: {self.data['consumable_enabled']}")
        if self.data['consumable_enabled'] == "reset all":
            print("Resetting all consumables")
            self.data['bonus_exp_cp'] = datetime.min
            self.data['regular_exp_cp'] = datetime.min
            self.data['legion_drop'] = datetime.min
            self.data['legion_meso'] = datetime.min
            self.data['wap'] = datetime.min
            self.data['eap'] = datetime.min
            self.data['consumable_enabled'] = "enabled"

        updated_already = False
        def setup_once_if_needed():
            nonlocal updated_already
            if updated_already: return False
            if not self.bot.update_use_inventory_region(dirty=True):
                print("Could not find inventory USE region")
            updated_already = True
            return True

        def cancel_if_needed():
            loc = common.locate_center_on_screen(Images.CANCEL, confidence=0.9, region=self.confirmation_dialog_region, grayscale=True)
            if loc:
                interception.click(loc)
                time.sleep(0.1)
                return True
            loc = common.locate_center_on_screen(Images.CONFIRM_CONSUMABLE_USED, confidence=0.9, grayscale=True)
            if loc:
                interception.click(loc)
                time.sleep(0.1)
                return True
            return False

        def randomize_loc_a_little(loc, range=5):
            return (loc[0] + random.randint(-range, range), loc[1] + random.randint(-range, range))

        cur = datetime.now()
        if cur > self.data['bonus_exp_cp']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.EXP_BONUS_CP, confidence=0.9, region=self.data['use_inventory_region'], grayscale=True)
            if loc:
                print("Bonus Exp CP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, delay=uniform(0.1, 0.15))
                self.data['bonus_exp_cp'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('bonus_exp_cp', self.data['bonus_exp_cp'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['regular_exp_cp']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.LEGION_EXP, confidence=0.9, region=self.data['use_inventory_region']) or \
                common.locate_center_on_screen(Images.EXP_REGULAR_2x, confidence=0.9, region=self.data['use_inventory_region']) or \
                common.locate_center_on_screen(Images.EXP_REGULAR_3x, confidence=0.9, region=self.data['use_inventory_region']) or \
                common.locate_center_on_screen(Images.EXP_REGULAR_MVP, confidence=0.9, region=self.data['use_inventory_region']) or \
                common.locate_center_on_screen(Images.EXP_REGULAR_MUGONG, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("Regular Exp CP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['regular_exp_cp'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('regular_exp_cp', self.data['regular_exp_cp'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['legion_drop']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.LEGION_DROP, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("Legion Drop")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['legion_drop'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('legion_drop', self.data['legion_drop'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['legion_meso']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.LEGION_MESO, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("Legion Mesos")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['legion_meso'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('legion_meso', self.data['legion_meso'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['wap']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.WAP, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("WAP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['wap'] = cur + timedelta(seconds=60 * 30 + 3)
                self.database.set('wap', self.data['wap'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['eap']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.EAP, confidence=0.95, region=self.data['use_inventory_region'])
            if loc:
                print("EAP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['eap'] = cur + timedelta(seconds=60 * 30 + 3)
                self.database.set('eap', self.data['eap'])
                sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                sleep(0.2)

        if cur > self.data['next_familiar_fuel']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.FAM_FUEL, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("Familiar Fuel")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2, interval=uniform(0.1, 0.15))
                self.data['next_familiar_fuel'] = cur + timedelta(hours=1)
            else:
                print("No familiar fuel found")

    def wheel(self):
        if self.should_exit(): return
        self.bot.press_release('a', 0.5)
        return True

    def erda_fountain(self, delayAfter=0.55, custom_cd=59):
        if self.should_exit(): return
        if datetime.now() > self.data['next_erda_fountain']:
            self.bot.press_release('b')
            self.bot.press_release('b')
            self.data['next_erda_fountain'] = datetime.now() + timedelta(seconds=custom_cd)
            self.database.set('next_erda_fountain', self.data['next_erda_fountain'])
            sleep(delayAfter)
            return True
        return False

    def janus(self, delayAfter=0.68):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus', self.data['next_janus'])
            sleep(delayAfter)
            return True
        return False

    def janus2(self, delayAfter=0.68):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus2']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus2'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus2', self.data['next_janus2'])
            sleep(delayAfter)
            return True
        return False
    
    def janus3(self, delayAfter=0.68):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus3']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus3'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus3', self.data['next_janus3'])
            sleep(delayAfter)
            return True
        return False

    def flash_jump(self, jumpDelay=0.25, delayAfter=0.7, extraPress=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        if (extraPress):
            self.bot.press_release('e', 0.05)
        self.bot.press_release('e', delayAfter)

    def jump_attack(self, attackDelay=0.2, jumpDelay=0.05, delayAfter=0.54, withSkill=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('e', attackDelay)
        self.bot.press_release('q')
        if withSkill:
            pass  # Placeholder for skill usage
        sleep(delayAfter)

    def jump_attack_still(self, attackDelay=0.05, delayAfter=0.67):
        if self.should_exit(): return
        self.bot.press_release('e', attackDelay)
        self.bot.press_release('q')
        sleep(delayAfter)

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

    def jump_down_attack_turn(self, attackDelay=0.06, delayAfter=1, turn='left'):
        if self.should_exit(): return
        self.bot.press('down', delay=0.04)
        self.bot.press('e', delay=0.04)
        if turn == 'left':
            self.bot.press_release('left', delay=0.02)
        else:
            self.bot.press_release('right', delay=0.02)
        sleep(attackDelay)
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

    def rope(self, delayAfter=2):
        if self.should_exit(): return
        self.bot.press_release('c', delayAfter)

    def default_macro(self):
      """Default macro for Ren class - placeholder implementation"""

      def setup():
        self.bot.press_release('right')
        self.flash_jump()
        self.bot.press_release('left')
        self.flash_jump()
        self.rope(delayAfter=2.5)
        self.wheel()
        self.bot.press('q')
        self.bot.press('left', delay=1)
        self.bot.release('left')
        self.flash_jump()
        self.bot.release('q', delay=0.2)
        self.flash_jump(delayAfter=0.9)
        self.erda_fountain()
        self.bot.press('left', delay=0.3)
        self.bot.release('left')
        self.flash_jump(jumpDelay=0.3)
        self.bot.press('left', delay=0.3)
        self.bot.release('left')
        self.janus()
        self.bot.press('q')
        self.flash_jump()
        self.flash_jump(delayAfter=1)
        self.bot.press('right')
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.jump_down()
        self.bot.release('right')
      
      def rotation():
        self.bot.press('left')
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.bot.release('left')
        self.bot.press('right')
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.flash_jump()
        self.bot.release('right')

      self.bot.press('q')
      while not self.should_exit():
        if datetime.now() > self.data['next_buff_check']:
          self.bot.release('q')
          self.buff_setup()
          self.data['next_buff_check'] = datetime.now() + timedelta(seconds=30)
          self.bot.press('q')
        if datetime.now() > self.data['next_erda_fountain']:
          self.bot.release('q')
          setup()
        # self.consumables_check()
        self.bot.release('q')
        self.bot.press('q')
        rotation()
      self.bot.release('q')

# OVERRIDES FOR RUNE BOT INTERFACE
    def rune_flash_jump(self):
        self.flash_jump()

    def rune_rope(self):
        self.rope()
    
    def rune_jump_down(self):
        self.jump_down()

    def rune_jump(self):
        self.bot.press_release('e')

    def rune_protect(self):
        return
    
    def rune_interact(self):
        self.bot.press_release('y')
# END OF OVERRIDES FOR RUNE BOT INTERFACE

if __name__=="__main__":
    try:
        ren = Ren()
        ren.main()
    except KeyboardInterrupt:
        state['running'] = False
        exit()

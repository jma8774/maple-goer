import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state
import common
from common import uniform
from rune.rune_abstract import RuneWalkerPilot
from rune.rune import RuneWalker
from database.database import Database
import interception


class DemonSlayer(RuneWalkerPilot):
    # Region definitions
    ascendion_region = (0, 200, 450, 500)
    firespirit_region = (0, 450, 700, 750-450)
    ebon_region = (750, 230, 1365-750, 415-230)
    gate1_region = (5, 300, 365-5, 545-300)
    alley3_region = (0, 310, 670, 725-310)
    summer5_region = (2, 408, 772-2, 652-408)
    bottompassage6_region = (10, 165, 608-10, 513-165)

    confirmation_dialog_region = (550, 310, 815-550, 477-310)

    def __init__(self):
        self.bot = None
        self.database = Database(db_path="data/jeemong_ds.json")
        self.data = {
            'next_erda_fountain': self.database.get('next_erda_fountain', datetime.now()),
            'next_janus': self.database.get('next_janus', datetime.now()),
            'next_janus2': self.database.get('next_janus2', datetime.now()),
            'whiteroomed': False,
            'is_paused': False,
            'next_boundless': self.database.get('next_boundless', datetime.now()),
            'next_orthus': self.database.get('next_orthus', datetime.now()),
            'next_chomp': datetime.now(),
            'next_demon_cry': datetime.now()
        }
        # Initialize script mapping
        self.scripts = {
            # "arcus": lambda: outlaw2_macro(self),
            # "odium": lambda: alley3_macro(self),
            # "shangrila": lambda: summer5_macro(self),
            # "arteria": lambda: bottomdeck6_macro(self),
            # "carcion": lambda: carcion_macro(self),
            "arcane_river": lambda: self.below_the_cave(),
            "default": lambda: self.below_the_cave()
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
            # "arcus": Images.ARCUS_ICON,
            # "odium": Images.ODIUM_ICON,
            # "shangrila": Images.SHANGRILA_ICON,
            # "arteria": Images.ARTERIA_ICON,
            # "carcion": Images.CARCION_ICON,
            "arcane_river": Images.ARTERIA_ICON,
            "default": Images.ARTERIA_ICON
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
        self.data['next_petfood'] = datetime.now() + timedelta(seconds=90)

    def consumable_setup(self):
        self.data['bonus_exp_cp'] = self.database.get('bonus_exp_cp', datetime.min)
        self.data['regular_exp_cp'] = self.database.get('regular_exp_cp', datetime.min) # This include Legion
        self.data['legion_drop'] = self.database.get('legion_drop', datetime.min)
        self.data['wap'] = self.database.get('wap', datetime.min)
        self.data['eap'] = self.database.get('eap', datetime.min)

    def should_exit(self, func=None):
        # XXX TODO: remove
        # If used as a function call without arguments
        if func is None:
            if False and state['checkmap'] and not self.data.get('whiteroomed', False) and common.pause_if_whiteroom(pag, self.data, self.getMap()):
                self.data['whiteroomed'] = True
            if self.data.get('is_paused', False):
                raise Exception("Stopping thread")
            return False
            
        # If used as a decorator
        def wrapper(*args, **kwargs):
            if False and state['checkmap'] and not self.data.get('whiteroomed', False) and common.pause_if_whiteroom(pag, self.data, self.getMap()):
                self.data['whiteroomed'] = True
            if self.data.get('is_paused', False):
                raise Exception("Stopping thread")
            if callable(func):
                return func(self, *args, **kwargs)
                
        return wrapper
 
    def buff_setup(self):
        if self.should_exit(): return
        # if self.bot.check_rune_and_walk():
        #     self.teleport_reset()
        #     return
        cur = datetime.now()
        
        self.bot.check_person_entered_map(only_guild=True)
        # self.bot.check_fam_leveling()
        # self.bot.check_tof("y")
        # self.bot.check_wap()
        # self.bot.check_fam_fuel()
        self.bot.check_elite_box()

        # if cur > self.data['next_petfood']:
        #   self.bot.press_release('f10')
        #   self.data['next_petfood'] = cur + timedelta(seconds=90)

        # if self.data['next_boundless']:
        #     self.bot.press_release('pageup', delay=0.7)
        #     self.data['next_boundless'] = cur + timedelta(seconds=120)

        if self.data['next_orthus']:
            self.bot.press_release('3', delay=0.7)
            self.data['next_orthus'] = cur + timedelta(seconds=120)

    def consumables_check(self):
        # if self.should_exit(): return
        if self.data['consumable_enabled'] == "disabled": return
        # "bonus_exp_cp", "regular_exp_cp", "legion_drop", "wap"
        # EXP_BONUS_CP      = openImage("exp_bonus.png")
        # EXP_REGULAR_MUGONG = openImage("exp_regular_mugong.png")
        # EXP_REGULAR_2x    = openImage("exp_regular_2x.png")
        # EXP_REGULAR_3x    = openImage("exp_regular_3x.png")
        # EXP_REGULAR_MVP   = openImage("exp_regular_mvp.png")

        # # Legion
        # LEGION_DROP       = openImage("legion_drop.png")
        # LEGION_EXP        = openImage("legion_exp.png")
        updated_already = False
        def setup_once_if_needed():
            nonlocal updated_already
            if updated_already: return
            # Update self.data['use_inventory_region']
            if not self.bot.update_use_inventory_region(dirty=True):
                print("Could not find inventory USE region")
            updated_already = True
            self.web(delayAfter=0.4)

        def cancel_if_needed():
            loc = common.locate_center_on_screen(Images.CANCEL, confidence=0.9, region=self.confirmation_dialog_region, grayscale=True)
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
                interception.click(loc, clicks=2)
                self.data['bonus_exp_cp'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('bonus_exp_cp', self.data['bonus_exp_cp'])
                time.sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                time.sleep(0.2)

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
                interception.click(loc, clicks=2)
                self.data['regular_exp_cp'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('regular_exp_cp', self.data['regular_exp_cp'])
                time.sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                time.sleep(0.2)

        if cur > self.data['legion_drop']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.LEGION_DROP, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("Legion Drop")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2)
                self.data['legion_drop'] = cur + timedelta(seconds=60 * 30 + 10)
                self.database.set('legion_drop', self.data['legion_drop'])
                time.sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                time.sleep(0.2)

        if cur > self.data['wap']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.WAP, confidence=0.9, region=self.data['use_inventory_region'])
            if loc:
                print("WAP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2)
                self.data['wap'] = cur + timedelta(seconds=60 * 30 + 3)
                self.database.set('wap', self.data['wap'])
                time.sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                time.sleep(0.2)

        if cur > self.data['eap']:
            setup_once_if_needed()
            loc = common.locate_center_on_screen(Images.EAP, confidence=0.95, region=self.data['use_inventory_region'])
            if loc:
                print("EAP")
                interception.move_to(randomize_loc_a_little(loc))
                interception.click(loc, clicks=2)
                self.data['eap'] = cur + timedelta(seconds=60 * 30 + 3)
                self.database.set('eap', self.data['eap'])
                time.sleep(0.15)
                cancel_if_needed()
                interception.move_to((uniform(600, 800), uniform(100, 200)))
                time.sleep(0.2)
                
    def below_the_cave(self):
      def rotation():
        self.bot.press_release('right')
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.bot.press_release('left')
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()
        self.jump_attack_demon_cry_and_chomp()

      print("Started DS Basic macro")
      while not self.should_exit():
          self.buff_setup()
          rotation()
      print("Paused DS Basic macro")
    
    def concussion(self, delayAfter=0.51):
        if self.should_exit(): return
        self.bot.press_release('q', delay=delayAfter)

    def chaos_lock(self, delayAfter=1):
        if self.should_exit(): return
        self.bot.press_release('x', delay=delayAfter)

    def chomp(self, delayAfter=0.5, custom_cd=5):
        if self.should_exit(): return
        if datetime.now() > self.data['next_chomp']:
            self.bot.press_release('f')
            self.bot.press_release('f')
            self.data['next_chomp'] = datetime.now() + timedelta(seconds=custom_cd)
            time.sleep(delayAfter)
            return True
        return False
    
    def demon_cry(self, delayAfter=0.5, custom_cd=6):
        if self.should_exit(): return
        if datetime.now() > self.data['next_demon_cry']:
            self.bot.press_release('r')
            self.data['next_demon_cry'] = datetime.now() + timedelta(seconds=custom_cd)
            time.sleep(delayAfter)
            return True
        return False
        
    def erda_fountain(self, delayAfter=0.5, custom_cd=59):
        if self.should_exit(): return
        if datetime.now() > self.data['next_erda_fountain']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_erda_fountain'] = datetime.now() + timedelta(seconds=custom_cd)
            self.database.set('next_erda_fountain', self.data['next_erda_fountain'])
            time.sleep(delayAfter)
            return True
        return False

    def janus(self, delayAfter=0.65):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus', self.data['next_janus'])
            time.sleep(delayAfter)
            return True
        return False

    def janus2(self, delayAfter=0.65):
        if self.should_exit(): return
        if datetime.now() > self.data['next_janus2']:
            self.bot.press_release('n')
            self.bot.press_release('n')
            self.data['next_janus2'] = datetime.now() + timedelta(seconds=59)
            self.database.set('next_janus2', self.data['next_janus2'])
            time.sleep(delayAfter)
            return True
        return False

    def flash_jump(self, jumpDelay=0.2, delayAfter=0.7):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('left')
        self.bot.press_release('left')
        self.bot.press_release('left')
        time.sleep(delayAfter)

    def jump_attack_demon_cry_and_chomp(self, attackDelay=0.2, jumpDelay=0.05, delayAfter=0.62):
        if self.should_exit(): return
        self.jump_attack(attackDelay, jumpDelay, delayAfter, use_demon_cry=True, use_chomp=True)

    def jump_attack(self, attackDelay=0.2, jumpDelay=0.05, delayAfter=0.62, use_demon_cry=False, use_chomp=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('e', attackDelay)
        if use_demon_cry and self.demon_cry(delayAfter=0.01):
            pass
        elif use_chomp and self.chomp(delayAfter=0.01):
            pass
        else:
            self.bot.press_release('q')
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

    def rope(self, delayAfter=2):
        if self.should_exit(): return
        self.bot.press_release('c', delayAfter)

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
      pass
    
    def rune_interact(self):
        self.bot.press_release('y')
# END OF OVERRIDES FOR RUNE BOT INTERFACE

if __name__=="__main__":
    try:
        demon_slayer = DemonSlayer()
        demon_slayer.main()
    except KeyboardInterrupt:
        state['running'] = False
        exit()

  
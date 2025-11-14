import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state
import common
from common import uniform, sleep
from marksman_src.map_outlaw2 import outlaw2_macro
from marksman_src.map_alley3 import alley3_macro
from marksman_src.map_summer5 import summer5_macro
from marksman_src.map_bottomdeck6 import bottomdeck6_macro
from marksman_src.map_gate1 import gate1_macro
from marksman_src.map_firespirit3 import firespirit3_macro
from marksman_src.map_carcion import carcion_macro
from marksman_src.map_calm_beach_3 import calm_beach_3_macro
from rune.rune_abstract import RuneWalkerPilot
from rune.rune import RuneWalker
from database.database import Database
import interception


class Marksman(RuneWalkerPilot):
    # Region definitions
    ascendion_region = (0, 200, 450, 500)
    firespirit_region = (0, 450, 700, 750-450)
    ebon_region = (750, 230, 1365-750, 415-230)
    gate1_region = (5, 300, 365-5, 545-300)
    alley3_region = (0, 310, 670, 725-310)
    summer5_region = (2, 408, 772-2, 652-408)
    bottompassage6_region = (10, 165, 608-10, 513-165)
    calm_beach_3_region = (363, 381, 983-363, 501-381)

    confirmation_dialog_region = (550, 310, 815-550, 477-310)

    def __init__(self):
        self.bot = None
        self.database = Database(db_path="data/jeemong_marksman.json")
        self.data = {
            'next_blink_setup': self.database.get('next_blink_setup', datetime.now()),
            'next_boss_buff': datetime.now() + timedelta(minutes=0.5),
            'next_surgebolt': datetime.now(),
            'next_web': datetime.now(),
            'next_solar_crest': datetime.now(),
            'next_high_speed': datetime.now(),
            'next_bolt_burst': datetime.now(),
            'next_erda_fountain': self.database.get('next_erda_fountain', datetime.now()),
            'next_janus': self.database.get('next_janus', datetime.now()),
            'next_janus2': self.database.get('next_janus2', datetime.now()),
            'next_janus3': self.database.get('next_janus3', datetime.now()),
            'next_loot_2': datetime.now() + timedelta(minutes=1.5),
            'next_familiar_fuel': datetime.now() + timedelta(hours=1),
            'whiteroomed': False,
            'is_paused': False
        }
        # Initialize script mapping
        self.scripts = {
            # "arcus": lambda: outlaw2_macro(self),
            # "odium": lambda: alley3_macro(self),
            # "shangrila": lambda: summer5_macro(self),
            "arteria": lambda: bottomdeck6_macro(self),
            "carcion": lambda: calm_beach_3_macro(self),
            "default": lambda: calm_beach_3_macro(self)
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
        self.data['next_petfood'] = datetime.now() + timedelta(seconds=90)

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
            self.teleport_reset(delayAfter=0.05)
            self.teleport_reset()
            return
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

        if cur > self.data['next_boss_buff'] and common.locate_on_screen(Images.ELITE_BOSS_HP, region=(200, 0, 1150-200, 30)):
            self.bot.press_release('t', 0.5)
            self.bot.press_release('pageup', 0.45)
            self.bot.press_release('home', 0.45)
            self.bot.press_release('insert', 0.9)
            self.bot.press_release('delete', 0.6)
            self.data['next_boss_buff'] = cur + timedelta(minutes=uniform(1.5, 1.7))

        if cur > self.data['next_blink_setup']:
            self.bot.press('down')
            self.bot.press_release('x')
            self.bot.press_release('x')
            self.bot.release('down', 0.6)
            self.data['next_blink_setup'] = cur + timedelta(seconds=uniform(35, 40))
            self.database.set('next_blink_setup', self.data['next_blink_setup'])

    def consumables_check(self):
        # if self.should_exit(): return
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
            if updated_already: return False
            # Update self.data['use_inventory_region']
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
                self.web(delayAfter=0.4)
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
                self.web(delayAfter=0.4)
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
                self.web(delayAfter=0.4)
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
                self.web(delayAfter=0.4)
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
                
    def shoot(self, delayAfter=0.51):
        if self.should_exit(): return
        self.bot.press_release('q', delay=delayAfter)

    def covering_fire(self, delayAfter=0.7):
        if self.should_exit(): return
        self.bot.press_release('shift', delay=delayAfter)

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

    def bolt_burst(self, delayAfter=0.5, isGo=True):
        if self.should_exit(): return
        if isGo and datetime.now() > self.data['next_bolt_burst']:
            self.bot.press_release('d', delay=delayAfter)
            self.data['next_bolt_burst'] = datetime.now() + timedelta(seconds=7-delayAfter)
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
    
    def solar_crest(self, delayAfter=0.4):
        if self.should_exit(): return
        if datetime.now() > self.data['next_solar_crest']:
            self.bot.press_release('5', delay=delayAfter)
            self.data['next_solar_crest'] = datetime.now() + timedelta(seconds=251)
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
            self.bot.press_release('f2', delay=delayAfter)
            self.data['next_high_speed'] = datetime.now() + timedelta(seconds=15)
            return True
        return False

    def flash_jump(self, jumpDelay=0.2, delayAfter=0.7, extraPress=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        if (extraPress):
            self.bot.press_release('e', 0.05)
        self.bot.press_release('e', delayAfter)

    def jump_attack(self, attackDelay=0.2, jumpDelay=0.05, delayAfter=0.54, withSurge=False):
        if self.should_exit(): return
        self.bot.press_release('e', jumpDelay)
        self.bot.press_release('e', attackDelay)
        self.bot.press_release('q')
        if withSurge:
            self.surgebolt()
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

    def surgebolt(self, delayAfter=0.07):
        if datetime.now() > self.data['next_surgebolt']:
            self.bot.press_release('r')
            self.data['next_surgebolt'] = datetime.now() + timedelta(seconds=10)
            sleep(delayAfter)
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
        if not self.solar_crest():
            self.web()
        sleep(0.3)
    
    def rune_interact(self):
        self.bot.press_release('y')
# END OF OVERRIDES FOR RUNE BOT INTERFACE

if __name__=="__main__":
    try:
        marksman = Marksman()
        marksman.main()
    except KeyboardInterrupt:
        state['running'] = False
        exit()

  
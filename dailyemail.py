import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state
import common
from common import uniform

ascendion_region = (0, 200, 450, 500)
firespirit_region = (0, 450, 700, 750-450)
ebon_region = (750, 230, 1365-750, 415-230)
gate1_region = (5, 300, 365-5, 545-300)
alley3_region = (0, 310, 670, 725-310)
summer5_region = (2, 408, 772-2, 652-408)

def getMap():
  maps = {
    "cernium": Images.CERNIUM_ICON,
    # "burnium": Images.BURNIUM_ICON,
    # "gate1": Images.ODIUM_ICON,
    "arcus": Images.ARCUS_ICON,
    "odium": Images.ODIUM_ICON,
    "shangrila": Images.SHANGRILA_ICON,
    "default": Images.SHANGRILA_ICON
  }
  return maps[state['script']] if state['script'] in maps else maps['default']

b = None
data = {
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

  'next_loot_2': datetime.now() + timedelta(minutes=1.5),
}

def main():
  global b

  scripts = {
    "cernium": firespirit3_macro,
    "arcus": outlaw2_macro,
    "odium": alley3_macro,
    "shangrila": summer5_macro,
    "default": summer5_macro,

    # "gate1": gate1_macro,
    # "burnium": ebonmage_macro,
  }
    
  config = {
    "user": "jeemong",
    "script": scripts[state['script']],
    "setup": setup,
  }
  b = BotBase(data, config, args=sys.argv, scripts=scripts)
  b.run()
    
def setup():
  data['x_and_down_x'] = True
  data['next_blink_setup'] = None
  data['next_split'] = datetime.now()
  data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(180, 220))
  data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 140))

def should_exit(func=None): # Use as a decorator or as a function by calling should_exit()
  def wrapper(*args, **kwargs):
    if state['checkmap'] and not data['whiteroomed'] and common.pause_if_whiteroom(pag, data, getMap()):
      data['whiteroomed'] = True
    if data['is_paused']:
      raise Exception("Stopping thread")
    if callable(func):
        func(*args, **kwargs)
  if callable(func):
    return wrapper
  return wrapper()

def summer5_macro():
  erda_seq = 0
  def loot():
    if datetime.now() < data['next_loot']:
      return
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    jump_down_attack_turn(delayAfter=0.5, turn='right')
    jump_down_attack(delayAfter=0.5)  
    jump_down_attack(delayAfter=0.5)
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    jump_up(delayBetween=0.4, delayAfter=0.4)
    bolt_burst()
    shoot()
    b.press_release('left')
    teleport_reset()
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

  def rotation():
    nonlocal erda_seq
    rng = random.random()
    # Find mob before starting rotation
    if state['scanmob']:
      mob_loc = None
      count = 0
      interval = 0.1
      while mob_loc == None:
        mob_loc = pag.locateOnScreen(Images.SUMMER5_MOB, confidence=0.95, grayscale=True, region=summer5_region) or pag.locateOnScreen(Images.SUMMER5_MOB2, confidence=0.95, grayscale=True, region=summer5_region)
        time.sleep(interval)
        count += 1
        if count > (6/interval): break # 6 seconds
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")

    jump_down_attack(attackDelay=0.3, delayAfter=0.40)
    b.press_release('right')
    shoot(delayAfter=0.53)
    jump_down_attack_turn(attackDelay=0.3, delayAfter=0.5, turn='left')
    b.press_release('right')
    if data['next_erda_fountain'] - timedelta(seconds=1) < datetime.now():
      jump_down(delayAfter=0.7)
      if erda_seq % 2 == 0:
        jump_down_attack(delayAfter=0.5)
        covering_fire(delayAfter=0.8)
      else:
        covering_fire()
        jump_down_attack(delayAfter=0.5)
      erda_seq += 1
      b.press('right', delay=0.3)
      b.release('right')
      erda_fountain()
      if not web():
        bolt_burst()
      b.press_release('left')
      teleport_reset()
    else:
      jump_attack(attackDelay=0.05, delayAfter=0.5)
      jump_attack(attackDelay=0.05, delayAfter=0.5)
      b.press_release('left')
      teleport_reset()
  
  print("Started Gentle Summer 5 macro")
  while not should_exit():
    buff_setup()
    rotation()
    loot()
  print("Paused Gentle Summer 5 macro")


def alley3_macro():
  erda_counter = 0
  def alley3_rotation():
    nonlocal erda_counter
    cur = datetime.now()
    # Use erda fountain if available
    if cur > data['next_erda_fountain']:
      erda_counter += 1
      jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
      if False:
        jump_down_attack(delayAfter=0.47)
        erda_fountain()
        teleport_reset()
      else:
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
        jump_down_attack_turn(delayAfter=0.45, turn='left')
        b.press('left', 0.7)
        b.release('left')
        erda_fountain()
        jump_down_attack(delayAfter=0.48)
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.53)
        b.press_release('right')
        teleport_reset()
        data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
    # Find mob before starting rotation
    if state['scanmob']:
      mob_loc = None
      count = 0
      interval = 0.1
      while mob_loc == None:
        mob_loc = pag.locateOnScreen(Images.ALLEY3_MOB, confidence=0.75, grayscale=True, region=alley3_region) or pag.locateOnScreen(Images.ALLEY3_MOB2, confidence=0.75, grayscale=True, region=alley3_region)
        time.sleep(interval)
        count += 1
        if count > (6/interval): break # 6 seconds
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")
    b.press_release('e', 0.15)
    q_and_surgebolt(afterDelay=0.52)
    b.press_release('left')
    jump_attack(attackDelay=0.05, delayAfter=0.51)
    jump_attack(attackDelay=0.05, delayAfter=0.77)
    if datetime.now() < data['next_loot']:
      jump_down_attack(delayAfter=0.45)
      b.press_release('right')
      jump_attack(attackDelay=0.05, delayAfter=0.51)
      jump_attack(attackDelay=0.05, delayAfter=0.53)
      teleport_reset()
    else:
      jump_up(delayAfter=1)
      b.press_release('right')
      data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
      teleport_reset()
  
  print("Started Alley 3 macro")
  while not should_exit():
    buff_setup()
    alley3_rotation()
  print("Paused Alley 3 macro")

def gate1_macro():
  def gate1_rotation():
    just_erda = False
    cur = datetime.now()
    # Use erda fountain if available
    if cur > data['next_erda_fountain']:
      b.press_release('shift', 0.8)
      erda_fountain()
      just_erda = True

    if just_erda:
      q_and_surgebolt(afterDelay=0.47)
      jump_down_attack_turn(delayAfter=0.45, turn='left')
      q_and_surgebolt(afterDelay=0.47)
      b.press_release('right')
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      teleport_reset()
    else:
      # Find mob before starting rotation
      if state['scanmob']:
        mob_loc = None
        count = 0
        interval = 0.15
        while mob_loc == None:
          mob_loc = pag.locateOnScreen(Images.DIAMOND_GUARDIAN1, confidence=0.75, grayscale=True, region=gate1_region) or pag.locateOnScreen(Images.DIAMOND_GUARDIAN2, confidence=0.75, grayscale=True, region=gate1_region)
          time.sleep(interval)
          count += 1
          if count > (6/interval): break # 6 seconds
        if mob_loc == None:
          print(f"Couldn't find mob after {count} tries, continuing rotation")
        else:
          print(f"Found mob at {mob_loc}, continuing rotation")
      q_and_surgebolt(afterDelay=0.47)
      jump_down_attack_turn(delayAfter=0.41, turn='left')
      jump_down_attack(delayAfter=0.41)
      b.press_release('right')
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      if random.random() > 0.6:
        jump_attack(attackDelay=0.05, delayAfter=0.47)
      teleport_reset()
  
  def gate1_loot():
    if datetime.now() < data['next_loot']:
      return
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    jump_down_attack(delayAfter=0.47)
    q_and_surgebolt(afterDelay=0.45)
    b.press_release('left')
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    b.press_release('c', 0.9)
    if not bolt_burst(0.6):
      if not web(delayAfter=0.6):
        q_and_surgebolt(afterDelay=0.6)
    b.press_release('right')
    if should_exit(): return
    teleport_reset()
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
    
  print("Started Road to the Castle's Gate 1 macro")
  while not should_exit():
    buff_setup()
    gate1_rotation()
    gate1_loot()
  print("Paused Road to the Castle's Gate 1 macro")

def outlaw2_macro():
  print("Started Outlaw Infested Wastes 2 macro")
  while not should_exit():
    buff_setup()
    q_and_surgebolt(afterDelay=0.55)
    jump_down_attack_turn(delayAfter=0.5, turn='right')
    q_and_surgebolt(afterDelay=0.55)
    b.press_release('left')
    jump_attack(attackDelay=0.05, delayAfter=0.55)
    jump_attack(attackDelay=0.05, delayAfter=0.55)
    teleport_reset()
  print("Paused Outlaw Infested Wastes 2 macro")

def ebonmage_macro():
  print("Started Ebon Mage macro")
  while not should_exit():
    if datetime.now() < data['next_loot']:
      buff_setup()
    else:
      jump_attack(jumpDelay=0.04, attackDelay=0.05, delayAfter=1)
      jump_down_attack(delayAfter=0.3)
      jump_down_attack_turn(delayAfter=0.4, turn='right')
      q_and_surgebolt(afterDelay=0.48)
      b.press_release('left')
      jump_attack(jumpDelay=0.04, attackDelay=0.05, delayAfter=0.47)
      teleport_reset()
      data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

    if datetime.now() > data['next_erda_fountain']:
      b.press('right', 0.8)
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      b.release('right')
      b.press_release('left')
      erda_fountain()
      jump_down_attack(delayAfter=0.5)
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      teleport_reset()
    else:
      if state['scanmob']:
        mob_loc = None
        count = 0
        interval = 0.15
        while mob_loc == None:
          mob_loc = pag.locateOnScreen(Images.EBON_MAGE1, confidence=0.75, grayscale=True, region=ebon_region) or pag.locateOnScreen(Images.EBON_MAGE2, confidence=0.75, grayscale=True, region=ebon_region)
          time.sleep(interval)
          count += 1
          if count > (6/interval): break # 6 seconds
        if mob_loc == None:
          print(f"Couldn't find mob after {count} tries, continuing rotation")
        else:
          print(f"Found mob at {mob_loc}, continuing rotation")
      shoot()
      jump_down_attack_turn(delayAfter=0.4, turn='right')
      shoot()
      jump_down_attack_turn(delayAfter=0.42, turn='left')
      q_and_surgebolt(afterDelay=0.47)
      b.press_release('right')
      q_and_surgebolt(afterDelay=0.47)
      b.press_release('left')
      teleport_reset()
  print("Paused Ebon Mage macro")
    
def firespirit3_macro():
  print("Started Fire Spirit 3 macro")
  while not should_exit():
    buff_setup()
    firespirit3_rotation()
    firespirit3_loot()
  print("Paused Fire Spirit 3 macro")

def firespirit3_rotation():
  cur = datetime.now()
  # Find mob before starting rotation
  if state['scanmob']:
    mob_loc = None
    count = 0
    interval = 0.15
    while mob_loc == None:
      mob_loc = pag.locateOnScreen(Images.FIRE_SPIRIT, confidence=0.75, grayscale=True, region=firespirit_region) or pag.locateOnScreen(Images.FIRE_SPIRIT2, confidence=0.75, grayscale=True, region=firespirit_region)
      time.sleep(interval)
      count += 1
      if count > (6/interval): break # 6 seconds
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")
    
  jump_down_attack(delayAfter=0.39)
  shoot()
  jump_down_attack_turn(delayAfter=0.44, turn='right')
  jump_down_attack(attackDelay=0.3, delayAfter=0.4)
  b.press_release('left')
  jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
  jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
  cur = datetime.now()
  if cur > data['next_erda_fountain']:
    jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.54)
    b.press_release('c', 1)
    if not bolt_burst(0.7):
      time.sleep(0.7)
    b.press_release('shift', 0.8)
    erda_fountain()
    if datetime.now() > data['next_loot_2']:
      time.sleep(0.4)
      data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
    teleport_reset()
  else:
    teleport_reset()
  
def firespirit3_loot():
  if datetime.now() < data['next_loot']:
    return
  jump_down_attack(delayAfter=0.7)
  jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.53)
  time.sleep(0.3)
  b.press_release('right')
  teleport_reset()
  jump_down_attack(delayAfter=0.7)
  jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.52)
  jump_down_attack(delayAfter=0.7)
  jump_down_attack_turn(delayAfter=0.36, turn='left')
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  b.check_rune()
  teleport_reset()
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

@should_exit
def buff_setup():
  cur = datetime.now()
  
  b.check_person_entered_map(only_guild=True)

  b.check_fam_leveling()
  
  b.check_tof("y")

  b.check_wap()

  b.check_fam_fuel()

  b.check_elite_box()

  b.check_rune()

  if cur > data['next_boss_buff'] and pag.locateOnScreen(Images.ELITE_BOSS_HP, region=(200, 0, 1150-200, 30)):
    b.press_release('t', 0.5)
    b.press_release('pageup', 0.45)
    b.press_release('home', 0.45)
    b.press_release('insert', 0.9)
    b.press_release('delete', 0.6)
    web(delayAfter=0.4)
    data['next_boss_buff'] = cur + timedelta(minutes=uniform(1.5, 1.7))

  if data['x_and_down_x']:
    teleport_reset()
    b.press('down')
    b.press_release('x')
    b.press_release('x')
    b.release('down', 0.6)
    data['x_and_down_x'] = False
    data['next_blink_setup'] = cur + timedelta(seconds=uniform(54, 58))
    return

  if data['next_blink_setup'] == None:
    teleport_reset()
    data['next_blink_setup'] = cur + timedelta(seconds=uniform(54, 58))
    return
  elif cur > data['next_blink_setup']:
    b.press('down')
    b.press_release('x')
    b.press_release('x')
    b.release('down', 0.6)
    data['next_blink_setup'] = cur + timedelta(seconds=uniform(54, 58))
    return

  if cur > data['next_split']:
    data['next_split'] = cur + timedelta(seconds=uniform(120, 140))
    b.press_release('2', 0.7)
    return

  # if cur > data['next_sharpeye']:
  #   data['next_sharpeye'] = cur + timedelta(seconds=uniform(180, 220))
  #   b.press_release('pagedown', 1.55)
  #   return

  # if cur > data['next_bird']:
  #   b.press_release('5', 0.7)
  #   data['next_bird'] = cur + timedelta(seconds=uniform(116, 125))

@should_exit
def shoot(delayAfter=0.51):
  b.press_release('q', delay=delayAfter)

@should_exit
def covering_fire(delayAfter=0.7):
  b.press_release('shift', delay=delayAfter)

@should_exit
def erda_fountain(delayAfter=0.5):
  if datetime.now() > data['next_erda_fountain']:
    b.press_release('b')
    b.press_release('b')
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    time.sleep(delayAfter)
    return True
  return False

@should_exit
def bolt_burst(delayAfter=0.5, isGo=True):
  if isGo and datetime.now() > data['next_bolt_burst']:
    b.press_release('d', delay=delayAfter)
    data['next_bolt_burst'] = datetime.now() + timedelta(seconds=7)
    return True
  return False

@should_exit
def jump_web(jumpDelay=0.2, delayAfter=0.3):
  if datetime.now() > data['next_web']:
    jump_down(delayAfter=jumpDelay)
    web(delayAfter=delayAfter)
    return True
  return False

@should_exit
def web(delayAfter=0.3):
  if datetime.now() > data['next_web']:
    b.press_release('4', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=251)
    return True
  return False

@should_exit
def jump_high_speed_shot(jumpDelay=0.2, delayAfter=0.3, isGo=True):
  if isGo and datetime.now() > data['next_high_speed']:
    jump_down(delayAfter=jumpDelay)
    high_speed_shot(delayAfter=delayAfter)
    return True
  return False

@should_exit
def high_speed_shot(delayAfter=0.3, isGo=True):
  if isGo and datetime.now() > data['next_high_speed']:
    b.press_release('a', delay=delayAfter)
    data['next_high_speed'] = datetime.now() + timedelta(seconds=15)
    return True
  return False

@should_exit
def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', delayAfter)

@should_exit
def jump_attack(attackDelay=0.2, jumpDelay=0.05, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', attackDelay)
  b.press_release('q')
  time.sleep(delayAfter)

@should_exit
def jump_up(delayBetween=0.2, delayAfter=1):
  b.press('up')
  b.press_release('e', delayBetween)
  b.press_release('e')
  b.press_release('e')
  b.release('up', delayAfter)

@should_exit
def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('e', 0.15)
  b.release('e')
  b.release('down', delayAfter)

@should_exit
def jump_down_attack(attackDelay=0.05, delayAfter=1):
  b.press('down')
  b.press('e', attackDelay)
  b.press_release('q')
  b.release('e')
  b.release('down', delayAfter)

  
@should_exit
def jump_down_attack_turn(attackDelay=0.05, delayAfter=1, turn='left'):
  b.press('down', delay=0.04)
  b.press('e', delay=0.04)
  if turn == 'left':
    b.press_release('left', delay=0.02)
  else:
    b.press_release('right', delay=0.02)
  time.sleep(attackDelay)
  b.press_release('q', delay=0.02)
  b.release('e', delay=0.02)
  b.release('down', delayAfter)

@should_exit
def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press('e')
  b.release('e')
  b.press('e')
  b.release('e', delayAfter)

@should_exit
def q_and_surgebolt(afterDelay=0.7):
  if datetime.now() > data['next_surgebolt']:
    b.press('q', delay=0.02)
    b.press_release('r')
    b.release('q', afterDelay)
    data['next_surgebolt'] = datetime.now() + timedelta(seconds=uniform(10, 13))
  else:
    b.press_release('q', afterDelay)

@should_exit
def teleport_reset(delayAfter=0.65):
  b.press_release('x')
  b.press_release('x', delayAfter)

if __name__=="__main__":
  main()
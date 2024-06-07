import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state

ascendion_region = (0, 200, 450, 500)
firespirit_region = (0, 450, 700, 750-450)
ebon_region = (750, 230, 1365-750, 415-230)
gate1_region = (5, 300, 365-5, 545-300)
alley3_region = (0, 310, 670, 725-310)
summer5_region = (2, 408, 772-2, 652-408)
minimap_map_icon_region = (0, 0, 55, 55)
def getMap():
  maps = {
    "liminia": Images.LIMINIA_ICON,
    "cernium": Images.CERNIUM_ICON,
    # "burnium": Images.BURNIUM_ICON,
    # "gate1": Images.ODIUM_ICON,
    "arcus": Images.ARCUS_ICON,
    "odium": Images.ODIUM_ICON,
    # "shangrila": Images.SHANGRILA_ICON,
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
    "liminia": midpoint3_macro,
    "cernium": firespirit3_macro,
    "arcus": outlaw2_macro,
    "odium": alley3_macro,
    # "shangrila": spring1_macro,
    "shangrila": summer5_macro,
    "default": summer5_macro,

    # "gate1": gate1_macro,
    # "burnium": ebonmage_macro,
    # "event": event_macro,
    # "tiru": tiru_macro,
    # "knight": knight_macro,
  }
    
  config = {
    "user": "jeemong",
    "script": scripts[state['script']],
    "setup": setup,
    "should_pause_cb": should_pause,
    "pause_cb": pause_cb
  }
  b = BotBase(data, config, args=sys.argv, scripts=scripts)
  b.run()
    
def setup():
  data['next_blink_setup'] = None
  data['next_split'] = datetime.now()
  data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(180, 220))
  data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 140))

def pause_cb():
  data['x_and_down_x'] = True


def summer5_macro():
  erda_seq = 0
  def loot():
    if datetime.now() < data['next_loot']:
      return
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    if should_pause(): return
    jump_down_attack_turn(delayAfter=0.5, turn='right')
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)  
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.5)
    if should_pause(): return
    jump_up(delayBetween=0.4, delayAfter=0.4)
    if should_pause(): return
    bolt_burst()
    if should_pause(): return
    shoot()
    if should_pause(): return
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
        if should_pause(): return
        mob_loc = pag.locateOnScreen(Images.SUMMER5_MOB, confidence=0.95, grayscale=True, region=summer5_region) or pag.locateOnScreen(Images.SUMMER5_MOB2, confidence=0.95, grayscale=True, region=summer5_region)
        time.sleep(interval)
        count += 1
        if count > (6/interval): break # 6 seconds
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")

    if should_pause(): return
    jump_down_attack(attackDelay=0.3, delayAfter=0.40)
    if should_pause(): return
    b.press_release('right')
    if should_pause(): return
    shoot()
    if should_pause(): return
    jump_down_attack_turn(attackDelay=0.3, delayAfter=0.5, turn='left')
    if should_pause(): return
    b.press_release('right')
    if data['next_erda_fountain'] - timedelta(seconds=1) < datetime.now():
      if should_pause(): return
      jump_down(delayAfter=0.7)
      if erda_seq % 2 == 0:
        if should_pause(): return
        jump_down_attack(delayAfter=0.5)
        if should_pause(): return
        covering_fire(delayAfter=0.8)
      else:
        if should_pause(): return
        covering_fire()
        if should_pause(): return
        jump_down_attack(delayAfter=0.5)
      erda_seq += 1
      if should_pause(): return
      b.press('right', delay=0.3)
      if should_pause(): return
      b.release('right')
      if should_pause(): return
      erda_fountain()
      if should_pause(): return
      b.press_release('left')
      teleport_reset()
    else:
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.5)
      if rng > 0.7:
        if should_pause(): return
        jump_attack(attackDelay=0.05, delayAfter=0.5)
      b.press_release('left')
      if should_pause(): return
      teleport_reset()
  
  print("Started Gentle Summer 5 macro")
  while not should_pause():
    buff_setup()
    rotation()
    loot()
  print("Paused Gentle Summer 5 macro")


def spring1_macro():
  print("Started Blooming Spring 1 macro")
  while not should_pause():
    buff_setup()
    if should_pause(): return
    b.press_release('e', 0.1)
    if should_pause(): return
    b.press_release('q', 0.6)
    if should_pause(): return
    b.press_release('q', 0.6)
    if should_pause(): return
    b.press_release('right')
    if should_pause(): return
    b.press_release('e', 0.1)
    if should_pause(): return
    b.press_release('q', 0.6)
    if should_pause(): return
    b.press_release('q', 0.6)
    if should_pause(): return
    b.press_release('left')
    teleport_reset()
    time.sleep(3)
  print("Paused Blooming Spring 1 macro")

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
        if should_pause(): return
        jump_down_attack(delayAfter=0.47)
        if should_pause(): return
        erda_fountain()
        if should_pause(): return
        teleport_reset()
      else:
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
        if should_pause(): return
        jump_down_attack_turn(delayAfter=0.45, turn='left')
        if should_pause(): return
        b.press('left', 0.7)
        if should_pause(): return
        b.release('left')
        if should_pause(): return
        erda_fountain()
        if should_pause(): return
        jump_down_attack(delayAfter=0.48)
        if should_pause(): return
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.51)
        if should_pause(): return
        jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.53)
        if should_pause(): return
        b.press_release('right')
        if should_pause(): return
        teleport_reset()
        data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
    # Find mob before starting rotation
    if state['scanmob']:
      mob_loc = None
      count = 0
      interval = 0.1
      while mob_loc == None:
        if should_pause(): return
        mob_loc = pag.locateOnScreen(Images.ALLEY3_MOB, confidence=0.75, grayscale=True, region=alley3_region) or pag.locateOnScreen(Images.ALLEY3_MOB2, confidence=0.75, grayscale=True, region=alley3_region)
        time.sleep(interval)
        count += 1
        if count > (6/interval): break # 6 seconds
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")
    if should_pause(): return
    b.press_release('e', 0.15)
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.52)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.51)
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.77)
    if datetime.now() < data['next_loot']:
      if should_pause(): return
      jump_down_attack(delayAfter=0.45)
      if should_pause(): return
      b.press_release('right')
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.51)
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.53)
      if should_pause(): return
      teleport_reset()
    else:
      jump_up(delayAfter=1)
      if should_pause(): return
      b.press_release('right')
      if should_pause(): return
      data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
      teleport_reset()
  
  print("Started Alley 3 macro")
  while not should_pause():
    buff_setup()
    alley3_rotation()
  print("Paused Alley 3 macro")

def gate1_macro():
  def gate1_rotation():
    just_erda = False
    cur = datetime.now()
    # Use erda fountain if available
    if cur > data['next_erda_fountain']:
      if should_pause(): return
      b.press_release('shift', 0.8)
      if should_pause(): return
      erda_fountain()
      just_erda = True

    if just_erda:
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.47)
      if should_pause(): return
      jump_down_attack_turn(delayAfter=0.45, turn='left')
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.47)
      if should_pause(): return
      b.press_release('right')
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      if should_pause(): return
      teleport_reset()
    else:
      # Find mob before starting rotation
      if state['scanmob']:
        mob_loc = None
        count = 0
        interval = 0.15
        while mob_loc == None:
          if should_pause(): return
          mob_loc = pag.locateOnScreen(Images.DIAMOND_GUARDIAN1, confidence=0.75, grayscale=True, region=gate1_region) or pag.locateOnScreen(Images.DIAMOND_GUARDIAN2, confidence=0.75, grayscale=True, region=gate1_region)
          time.sleep(interval)
          count += 1
          if count > (6/interval): break # 6 seconds
        if mob_loc == None:
          print(f"Couldn't find mob after {count} tries, continuing rotation")
        else:
          print(f"Found mob at {mob_loc}, continuing rotation")
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.47)
      if should_pause(): return
      jump_down_attack_turn(delayAfter=0.41, turn='left')
      if should_pause(): return
      jump_down_attack(delayAfter=0.41)
      if should_pause(): return
      b.press_release('right')
      if should_pause(): return
      jump_attack(attackDelay=0.05, delayAfter=0.47)
      if should_pause(): return
      if random.random() > 0.6:
        jump_attack(attackDelay=0.05, delayAfter=0.47)
      if should_pause(): return
      teleport_reset()
  
  def gate1_loot():
    if datetime.now() < data['next_loot']:
      return
    if should_pause(): return
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    if should_pause(): return
    jump_down_attack(delayAfter=0.47)
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.45)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    if should_pause(): return
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    if should_pause(): return
    jump_attack(jumpDelay=0.07, attackDelay=0.05, delayAfter=0.47)
    if should_pause(): return
    b.press_release('c', 0.9)
    if not bolt_burst(0.6):
      if not web(delayAfter=0.6):
        q_and_surgebolt(afterDelay=0.6)
    b.press_release('right')
    if should_pause(): return
    teleport_reset()
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   
    
  print("Started Road to the Castle's Gate 1 macro")
  while not should_pause():
    buff_setup()
    gate1_rotation()
    gate1_loot()
  print("Paused Road to the Castle's Gate 1 macro")

def outlaw2_macro():
  print("Started Outlaw Infested Wastes 2 macro")
  while not should_pause():
    buff_setup()
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.55)
    if should_pause(): return
    jump_down_attack_turn(delayAfter=0.5, turn='right')
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.55)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.55)
    if should_pause(): return
    jump_attack(attackDelay=0.05, delayAfter=0.55)
    if should_pause(): return
    teleport_reset()
  print("Paused Outlaw Infested Wastes 2 macro")

def ebonmage_macro():
  print("Started Ebon Mage macro")
  while not should_pause():
    if datetime.now() < data['next_loot']:
      buff_setup()
    else:
      if should_pause(): return
      jump_attack(jumpDelay=0.04, attackDelay=0.05, delayAfter=1)
      if should_pause(): return
      jump_down_attack(delayAfter=0.3)
      if should_pause(): return
      jump_down_attack_turn(delayAfter=0.4, turn='right')
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.48)
      if should_pause(): return
      b.press_release('left')
      jump_attack(jumpDelay=0.04, attackDelay=0.05, delayAfter=0.47)
      if should_pause(): return
      teleport_reset()
      data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

    if datetime.now() > data['next_erda_fountain']:
      if should_pause(): return
      b.press('right', 0.8)
      if should_pause(): return
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      if should_pause(): return
      b.release('right')
      if should_pause(): return
      b.press_release('left')
      if should_pause(): return
      erda_fountain()
      if should_pause(): return
      jump_down_attack(delayAfter=0.5)
      if should_pause(): return
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      if should_pause(): return
      jump_attack(jumpDelay=0.02, attackDelay=0.02, delayAfter=0.47)
      teleport_reset()
    else:
      if state['scanmob']:
        mob_loc = None
        count = 0
        interval = 0.15
        while mob_loc == None:
          if should_pause(): return
          mob_loc = pag.locateOnScreen(Images.EBON_MAGE1, confidence=0.75, grayscale=True, region=ebon_region) or pag.locateOnScreen(Images.EBON_MAGE2, confidence=0.75, grayscale=True, region=ebon_region)
          time.sleep(interval)
          count += 1
          if count > (6/interval): break # 6 seconds
        if mob_loc == None:
          print(f"Couldn't find mob after {count} tries, continuing rotation")
        else:
          print(f"Found mob at {mob_loc}, continuing rotation")
      if should_pause(): return
      b.press_release('q', 0.46)
      if should_pause(): return
      jump_down_attack_turn(delayAfter=0.4, turn='right')
      if should_pause(): return
      b.press_release('q', 0.46)
      if should_pause(): return
      jump_down_attack_turn(delayAfter=0.42, turn='left')
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.47)
      if should_pause(): return
      b.press_release('right')
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.47)
      if should_pause(): return
      b.press_release('left')
      teleport_reset()
  print("Paused Ebon Mage macro")
    
def firespirit3_macro():
  print("Started Fire Spirit 3 macro")
  while not should_pause():
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
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.FIRE_SPIRIT, confidence=0.75, grayscale=True, region=firespirit_region) or pag.locateOnScreen(Images.FIRE_SPIRIT2, confidence=0.75, grayscale=True, region=firespirit_region)
      time.sleep(interval)
      count += 1
      if count > (6/interval): break # 6 seconds
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")
    
  if should_pause(): return
  jump_down_attack(delayAfter=0.39)
  if should_pause(): return
  b.press_release('q', 0.50)
  if should_pause(): return
  jump_down_attack_turn(delayAfter=0.44, turn='right')
  if should_pause(): return
  jump_down_attack(attackDelay=0.3, delayAfter=0.4)
  if should_pause(): return
  b.press_release('left')
  if should_pause(): return
  jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
  if should_pause(): return
  jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.52)
  cur = datetime.now()
  if cur > data['next_erda_fountain']:
    if should_pause(): return
    jump_attack(jumpDelay=0.15, attackDelay=0.05, delayAfter=0.54)
    if should_pause(): return
    b.press_release('c', 1)
    if not bolt_burst(0.7):
      time.sleep(0.7)
      if should_pause(): return
    b.press_release('shift', 0.8)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    if datetime.now() > data['next_loot_2']:
      time.sleep(0.4)
      data['next_loot_2'] = datetime.now() + timedelta(minutes=1.5)
    teleport_reset()
  else:
    if should_pause(): return
    teleport_reset()
  
def firespirit3_loot():
  if datetime.now() < data['next_loot']:
    return
  if should_pause(): return
  jump_down_attack(delayAfter=0.7)
  if should_pause(): return
  jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.53)
  if should_pause(): return
  time.sleep(0.3)
  if should_pause(): return
  b.press_release('right')
  if should_pause(): return
  teleport_reset()
  if should_pause(): return
  jump_down_attack(delayAfter=0.7)
  if should_pause(): return
  jump_attack(jumpDelay=0.08, attackDelay=0.05, delayAfter=0.52)
  if should_pause(): return
  jump_down_attack(delayAfter=0.7)
  if should_pause(): return
  jump_down_attack_turn(delayAfter=0.36, turn='left')
  if should_pause(): return
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  if should_pause(): return
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  if should_pause(): return
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  if should_pause(): return
  b.check_rune()
  if should_pause(): return
  teleport_reset()
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))   

def midpoint3_macro():
  # buff_setup()
  # return
  print("Started World's Sorrow Midpoint 3 macro")
  while not should_pause():
    if data['x_and_down_x'] or datetime.now() < data['next_erda_fountain']:
      buff_setup()
    midpoint3_rotation()
    midpoint3_loot()
  print("Paused World's Sorrow Midpoint 3 macro")
    
def midpoint3_rotation():
  mob_loc = None
  rng = random.random()
  if datetime.now() > data['next_erda_fountain']:
    if should_pause(): return
    b.press_release('shift', 1)
    b.press('right', 0.3)
    b.release('right')
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    teleport_reset()
  else:
    # Find mob before starting rotation
    count = 0
    while mob_loc == None:
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.75, grayscale=True, region=ascendion_region)
      time.sleep(0.2)
      count += 1
      if count > 30: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")

  if should_pause(): return
  jump_down_attack(delayAfter=0.4)
  if should_pause(): return
  q_and_surgebolt(afterDelay=0.5)
  if should_pause(): return
  q_and_surgebolt(afterDelay=0.63)
  if should_pause(): return
  b.press_release('right')
  if not high_speed_shot(0.75, rng > 0.8):
    q_and_surgebolt(afterDelay=0.65)

def midpoint3_loot():
  loot_variation = int(random.random() * 3)
  
  def face_left_teleport_reset():
    if should_pause(): return
    b.press_release('left', delay=uniform(0.01, 0.05))
    if should_pause(): return
    teleport_reset()

  if datetime.now() < data['next_loot']:
    face_left_teleport_reset()
    return
  
  rng = random.random()
  rng2 = random.random()
  def right_part():
    if should_pause(): return
    b.press_release('shift', 1)
    b.press('right', 0.1)
    b.release('right')
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_down(delayAfter=0.1)
    if should_pause(): return
    if not bolt_burst(0.6, rng < 0.5):
      q_and_surgebolt(afterDelay=0.6)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    jump_down(delayAfter=0.6)
    if should_pause(): return
    jump_down_attack(delayAfter=0.7)
    if should_pause(): return
    if not jump_high_speed_shot(delayAfter=0.5, isGo=rng2 > 0.5):
      jump_down_attack(delayAfter=0.5)
    b.press_release('right', 0.1)
    if should_pause(): return
    if not jump_web(delayAfter=1.2):
      if should_pause(): return
      jump_down(delayAfter=1.2)
    if should_pause(): return
    face_left_teleport_reset()

  def left_part():
    if should_pause(): return
    if pag.locateOnScreen(Images.ASCENDION, confidence=0.75, grayscale=True, region=ascendion_region):
      q_and_surgebolt(afterDelay=0.5)
    if should_pause(): return
    b.press('left', 1.4)
    if should_pause(): return
    b.release('left', 0.3)
    b.press_release('right')
    if should_pause(): return
    if not jump_web(delayAfter=0.8):
      if should_pause(): return
      jump_down(delayAfter=0.4)
    if should_pause(): return
    jump_down_attack(delayAfter=0.7)
    if should_pause(): return
    jump_down(delayAfter=0.4)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_down(delayAfter=0.1)
    if should_pause(): return
    if not bolt_burst(1.5, rng >= 0.5):
      if should_pause(): return
      q_and_surgebolt(afterDelay=1.5)
    if should_pause(): return
    teleport_reset()

  if loot_variation == 0:
    if should_pause(): return
    face_left_teleport_reset()
    if should_pause(): return
    right_part()
    if should_pause(): return
    left_part()
  elif loot_variation == 1:
    if should_pause(): return
    face_left_teleport_reset()
    if should_pause(): return
    left_part()
    if should_pause(): return
    right_part()
  else:
    if should_pause(): return
    b.press('left', 1.4)
    if should_pause(): return
    b.release('left', 0.7)
    b.press_release('c', 1.4)
    if should_pause(): return
    if not bolt_burst(0.7):
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.7)
    b.press_release('right')
    if should_pause(): return
    jump_down(delayAfter=0.5)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    jump_down(delayAfter=0.6)
    if should_pause(): return
    teleport_reset()
    if should_pause(): return
    right_part()

  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))

def knight_macro():
  while not should_pause():
    buff_setup()
    jump_down_attack(delayAfter=0.6)
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.5)
    if datetime.now() > data['next_loot']:
        data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))
        jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
        jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
    teleport_reset()

def tiru_macro():
  while not should_pause():
    buff_setup()
    if datetime.now() > data['next_loot']:
      flash_jump(jumpDelay=0.1)
      data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.8))
    jump_down_attack(delayAfter=0.6)
    if should_pause(): return
    jump_down_attack(delayAfter=0.6)
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.5)
    if should_pause(): return
    b.press_release('right')
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.5)
    if should_pause(): return
    b.press_release('left')
    if should_pause(): return
    teleport_reset()

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

def shoot(delayAfter=0.51):
  b.press_release('q', delay=delayAfter)

def covering_fire(delayAfter=0.7):
  b.press_release('shift', delay=delayAfter)

def erda_fountain(delayAfter=0.5):
  if datetime.now() > data['next_erda_fountain']:
    b.press_release('b')
    b.press_release('b')
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    time.sleep(delayAfter)
    return True
  return False

def bolt_burst(delayAfter=0.5, isGo=True):
  if isGo and datetime.now() > data['next_bolt_burst']:
    b.press_release('d', delay=delayAfter)
    data['next_bolt_burst'] = datetime.now() + timedelta(seconds=7)
    return True
  return False

def jump_web(jumpDelay=0.2, delayAfter=0.3):
  if datetime.now() > data['next_web']:
    jump_down(delayAfter=jumpDelay)
    web(delayAfter=delayAfter)
    return True
  return False

def web(delayAfter=0.3):
  if datetime.now() > data['next_web']:
    b.press_release('4', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=251)
    return True
  return False

def jump_high_speed_shot(jumpDelay=0.2, delayAfter=0.3, isGo=True):
  if isGo and datetime.now() > data['next_high_speed']:
    jump_down(delayAfter=jumpDelay)
    high_speed_shot(delayAfter=delayAfter)
    return True
  return False

def high_speed_shot(delayAfter=0.3, isGo=True):
  if isGo and datetime.now() > data['next_high_speed']:
    b.press_release('a', delay=delayAfter)
    data['next_high_speed'] = datetime.now() + timedelta(seconds=15)
    return True
  return False

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', delayAfter)

def jump_attack(attackDelay=0.2, jumpDelay=0.05, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', attackDelay)
  b.press_release('q')
  time.sleep(delayAfter)

def jump_up(delayBetween=0.2, delayAfter=1):
  b.press('up')
  b.press_release('e', delayBetween)
  b.press_release('e')
  b.press_release('e')
  b.release('up', delayAfter)

def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('e', 0.15)
  b.release('e')
  b.release('down', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  b.press('down')
  b.press('e', attackDelay)
  b.press_release('q')
  b.release('e')
  b.release('down', delayAfter)

  
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

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press('e')
  b.release('e')
  b.press('e')
  b.release('e', delayAfter)

def q_and_surgebolt(afterDelay=0.7):
  if datetime.now() > data['next_surgebolt']:
    b.press('q', delay=0.02)
    b.press_release('r')
    b.release('q', afterDelay)
    data['next_surgebolt'] = datetime.now() + timedelta(seconds=uniform(10, 13))
  else:
    b.press_release('q', afterDelay)

def teleport_reset(delayAfter=0.65):
  if should_pause(): return
  b.press_release('x')
  if should_pause(): return
  b.press_release('x', delayAfter)

def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if state['checkmap'] and not data['is_changed_map'] and pause_if_change_map(getMap()):
    data['is_changed_map'] = True
  return data['is_paused']

def pause_if_change_map(map):
  isSeeMap = pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    if pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

if __name__=="__main__":
  main()
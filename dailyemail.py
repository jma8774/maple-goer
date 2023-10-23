import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state

ascendion_region = (0, 200, 450, 500)
firespirit_region = (0, 450, 700, 750-450)
minimap_map_icon_region = (5, 15, 40, 40)
map = Images.CERNIUM_ICON

b = None
data = {
  'x_and_down_x': False,
  'next_sharpeye': datetime.now(),
  'next_split': datetime.now(),
  'next_blink_setup': None,
  'next_bird': datetime.now(),

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
    "mp": midpoint3_macro,
    "fs": firespirit3_macro,
    "default": firespirit3_macro
  }

  for arg in sys.argv:
    if arg == 'nomap':
      state['checkmap'] = False
    elif arg == 'nomobscan':
      state['scanmob'] = False
    elif arg == 'nostatus':
      state['sendstatus'] = False
    elif arg == 'dev':
      state['checkmap'] = False
      state['scanmob'] = False
      state['sendstatus'] = False
    elif arg in scripts:
      state['script'] = arg
    
  def pause_cb():
    data['x_and_down_x'] = True

  b = BotBase(data, {
    "user": "jeemong",
    "script": scripts[state['script']],
    "setup": setup,
    "pause_cb": pause_cb
  })
  print(state)
  b.run()
    
def setup():
  data['next_blink_setup'] = None
  data['next_split'] = datetime.now()
  data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(180, 220))
  data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 140))
  
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
  jump_down_attack(delayAfter=0.37)
  if should_pause(): return
  b.press_release('q', 0.45)
  if should_pause(): return
  jump_down_attack_turn(delayAfter=0.34, turn='right')
  if should_pause(): return
  jump_down_attack(attackDelay=0.3, delayAfter=0.33)
  if should_pause(): return
  b.press_release('left')
  if should_pause(): return
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  if should_pause(): return
  jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.47)
  cur = datetime.now()
  if cur > data['next_erda_fountain']:
    if should_pause(): return
    jump_attack(jumpDelay=0.11, attackDelay=0.05, delayAfter=0.49)
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

def buff_setup():
  cur = datetime.now()
  
  b.check_person_entered_map()

  b.check_fam_leveling()
  
  b.check_tof("y")

  b.check_wap()

  b.check_fam_fuel()

  b.check_elite_box()

  b.check_rune()


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

  if cur > data['next_sharpeye']:
    data['next_sharpeye'] = cur + timedelta(seconds=uniform(180, 220))
    b.press_release('pagedown', 1.55)
    return

  if cur > data['next_bird']:
    b.press_release('5', 0.7)
    data['next_bird'] = cur + timedelta(seconds=uniform(116, 125))

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('f')
    b.press_release('f')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def bolt_burst(delayAfter=0.05, isGo=True):
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

def jump_up(delayAfter=1):
  b.press('up')
  b.press_release('e', 0.2)
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
  b.press('down')
  b.press('e')
  if turn == 'left':
    b.press_release('left')
  else:
    b.press_release('right')
  time.sleep(attackDelay)
  b.press_release('q')
  b.release('e')
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
  if state['checkmap'] and not data['is_changed_map'] and pause_if_change_map(map):
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
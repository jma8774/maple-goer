import time
import random
from datetime import datetime, timedelta
import pyautogui as pag
import os
from base import BotBase, Images, Audio, KeyListener, post_status

monster_region = (550, 20, 810, 290)
minimap_map_icon_region = (5, 15, 40, 40)
map_icon = None

b = None
data = {
  'next_erda_fountain': datetime.now(),
  'next_omen': datetime.now(),
  'next_buff': datetime.now(),
  'next_shuriken': datetime.now(),
}

def main():
  global b
  b = BotBase(data, {
    "user": "jeemong",
    "script": hidden_train_macro,
  })
  b.run()

def hidden_train_macro():
  global map_icon
  map_icon = Images.REVERSE_ICON
  print("Starting Hidden Research Train macro")
  while not should_pause():
    if datetime.now() > data['next_buff']:
      b.press_release('pagedown', 1.8)
      data['next_buff'] = datetime.now() + timedelta(seconds=90)
    b.check_rune()
    hidden_train_rotation()

def hidden_train_rotation():
  if datetime.now() >= data['next_erda_fountain']:
    jump_attack(delayAfter=1)
    if should_pause(): return
    b.press_release('shift', 0.6)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
  else:
    jump_attack()
    if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  b.press_release('left')
  jump_attack()
  if should_pause(): return
  jump_attack(useShuriken=True)
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  b.press_release('right')

def below_the_cave_macro():
  global map_icon
  map_icon = Images.VANISHING_ICON
  print("Starting 1-5 macro")
  while not should_pause():
    if datetime.now() > data['next_buff']:
      b.press_release('pagedown', 0.8)
      data['next_buff'] = datetime.now() + timedelta(seconds=90)
    b.check_rune()
    below_the_cave_rotation()

def below_the_cave_rotation():
  # Find mob before starting rotation
  # count = 0
  # mob_loc = None
  # while mob_loc == None:
  #   if should_pause(): return
  #   mob_loc = pag.locateOnScreen(Images.FOREBERION, confidence=0.75, grayscale=True, region=monster_region)
  #   time.sleep(0.3)
  #   count += 1
  #   if count > 20: break
  # if mob_loc == None:
  #   print(f"Couldn't find mob after {count} tries, continuing rotation")
  # else:
  #   print(f"Found mob at {mob_loc}, continuing rotation")
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  b.press_release('left')
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  b.press_release('right')

def omen():
  if datetime.now() > data['next_omen']:
    b.press_release('2')
    data['next_omen'] = datetime.now() + timedelta(seconds=60)
    return True
  return False
  
def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('f1')
    b.press_release('f1')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  b.press('down')
  b.press('e', attackDelay)
  b.press_release('q')
  b.release('e')
  b.release('down', delayAfter)

def jump_attack(attackDelay=0.01, jumpDelay=0.01, delayAfter=0.5, useShuriken=False):
  b.press_release('e', jumpDelay)
  b.press_release('e', attackDelay)
  if useShuriken and datetime.now() > data['next_shuriken']:
    b.press_release('a')
    data['next_shuriken'] = datetime.now() + timedelta(seconds=25)
  else:
    b.press_release('q')
  time.sleep(delayAfter)

def jump_up(delayAfter=1):
  b.press('up')
  b.press_release('w', 0.2)
  b.press_release('w')
  b.press_release('w')
  b.release('up', delayAfter)

def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('w', 0.15)
  b.release('w')
  b.release('down', delayAfter)

def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['whiteroomed'] and pause_if_change_map(map_icon):
    data['whiteroomed'] = True
  return data['is_paused']

def pause_if_change_map(map):
  isSeeMap = pag.locateOnScreen(map, confidence=0.55, region=minimap_map_icon_region, grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    if pag.locateOnScreen(map, confidence=0.55, region=minimap_map_icon_region, grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False
  
def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

main()
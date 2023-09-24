import time
import random
from datetime import datetime, timedelta
import pyautogui as pag
import os
from base import BotBase, Images, Audio, KeyListener, post_status

monster_region = (550, 20, 810, 290)
minimap_map_icon_region = (5, 15, 40, 40)

b = None
data = {
  'dragon_finished_action': datetime.now(),
  'next_fire_floor': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_fire_breath': datetime.now(),
  'next_wind_breath': datetime.now(),
  'next_dark_fog': datetime.now(),
  'next_onyx_dragon': datetime.now(),
  'next_web': datetime.now(),
}

def main():
  global b
  b = BotBase(data, {
    "user": "ricky",
    "script": liminia_1_5_macro,
  })
  b.run()

def liminia_1_5_macro():
  print("Starting 1-5 macro")
  while not should_pause():
    b.check_fam_leveling(fam_menu_key='o', summon_fam_key='f6')
    b.check_tof("space")
    b.check_wap()
    b.check_fam_fuel()
    b.check_rune()
    b.check_elite_box(boxkey='f12')
    liminia_1_5_rotation()

def liminia_1_5_rotation():
  # Find mob before starting rotation
  count = 0
  mob_loc = None
  while mob_loc == None:
    if should_pause(): return
    mob_loc = pag.locateOnScreen(Images.FOREBERION, confidence=0.75, grayscale=True, region=monster_region)
    time.sleep(0.3)
    count += 1
    if count > 20: break
  if mob_loc == None:
    print(f"Couldn't find mob after {count} tries, continuing rotation")
  else:
    print(f"Found mob at {mob_loc}, continuing rotation")

  if fire_breath():
    if datetime.now() > data['next_fire_floor']:
      b.press('left')
      if should_pause(): return
      teleport()
      if should_pause(): return
      teleport()
      if should_pause(): return
      teleport()
      if should_pause(): return
      b.press_release('ctrl')
      if should_pause(): return
      b.release('left')
      if should_pause(): return
      if datetime.now() > data['next_erda_fountain']:
        b.press('left')
        teleport()
        if should_pause(): return
        b.release('left')
        if should_pause(): return
        erda_fountain()
        b.press('right')
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        b.release('right')
        b.press_release('left')
        if should_pause(): return
      else:
        b.press('right')
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        b.release('right')
        if should_pause(): return
        b.press_release('left')
        if should_pause(): return
      data['next_fire_floor'] = datetime.now() + timedelta(seconds=uniform(15, 20))
    else:
      dark_fog()
      if not liminia_1_5_loot():
        time.sleep(2)
  else:
    wind_breath()
    dark_fog()
    if not liminia_1_5_loot():
      time.sleep(2)

def liminia_1_5_loot():
  if datetime.now() < data['next_loot']:
    return False
  if should_pause(): return
  b.press('up')
  if should_pause(): return
  teleport()
  if should_pause(): return
  b.release('up')
  if should_pause(): return
  b.press('left', 2)
  if should_pause(): return
  b.release('left')

  # Use spider web or onyx on top
  if not summon_web():
    if datetime.now() > data['next_onyx_dragon']:
      if should_pause(): return
      b.press('up')
      if should_pause(): return
      teleport()
      if should_pause(): return
      b.release('up')
      if should_pause(): return
      summon_onyx()
      if should_pause(): return
      b.press('down')
      if should_pause(): return
      teleport()
      if should_pause(): return
      b.release('down')

  if should_pause(): return
  b.press('down')
  if should_pause(): return
  teleport()
  b.release('down')
  if should_pause(): return
  b.press('right')
  if should_pause(): return
  teleport()
  if should_pause(): return
  teleport()
  # # if should_pause(): return
  # # teleport()
  if should_pause(): return
  b.release('right')
  if should_pause(): return
  b.press_release('left')
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.3, 1.7))
  return True
  
def dark_fog():
  if datetime.now() < data['next_dark_fog']:
    return
  b.press_release('pagedown', 0.7)
  data['next_dark_fog'] = datetime.now() + timedelta(seconds=uniform(40, 50))
  
def fire_breath():
  if datetime.now() > data['next_fire_breath']:
    if datetime.now() < data['dragon_finished_action']:
      b.press_release('ctrl')
    b.press_release('g')
    b.press_release('t', 0.7)
    data['next_fire_breath'] = datetime.now() + timedelta(seconds=10)
    data['dragon_finished_action'] = datetime.now() + timedelta(seconds=5)
    return True
  return False
  
def wind_breath():
  if datetime.now() > data['next_wind_breath']:
    if datetime.now() < data['dragon_finished_action']:
      data['next_fire_breath'] = datetime.now()
      b.press_release('ctrl')
    b.press_release('a')
    b.press_release('f', 0.7)
    data['next_wind_breath'] = datetime.now() + timedelta(seconds=8)
    data['dragon_finished_action'] = datetime.now() + timedelta(seconds=5)
    return True
  return False

def summon_onyx():
  if datetime.now() > data['next_onyx_dragon']:
    b.press_release('4')
    b.press_release('4', 0.8)
    data['next_onyx_dragon'] = datetime.now() + timedelta(seconds=80)
    return True
  return False

def summon_web():
  if datetime.now() > data['next_web']:
    b.press_release('delete')
    b.press_release('delete', 0.8)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False

def teleport(delay=0.6):
  b.press_release('d', delay)

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('x')
    b.press_release('x')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)

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
  if not data['is_changed_map'] and pause_if_change_map(Images.LIMINIA_ICON):
    data['is_changed_map'] = True
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
import time
import random
import threading
import pygame
import pyautogui as pag
from datetime import datetime, timedelta
import os
from base import BotBase, Images, Audio, KeyListener, post_status
import interception
key_pressed = {}

START_KEY = 'f7'
PAUSE_KEY = 'f8'

monster_region = (800, 0, 600, 300)
minimap_map_icon_region = (5, 15, 40, 40)

thread = None
b = None
data = {
  'next_gale_barrier': datetime.now(),
  'next_monsoon': datetime.now(),
  'next_sphere': datetime.now(),
  'next_merciless_wind': datetime.now(),
  'next_howling': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_phalanx_charge': datetime.now(),
  'next_web': datetime.now(),
  'next_cast': datetime.now(),
}

def main():
  global b
  b = BotBase(data, {
    "user": "justin",
    "script": end_1_5_macro,
  })
  b.run()

def end_1_5_macro():
  print("Started End of World 1-5 macro")
  while not should_pause():
    b.check_rune(play_sound=False)
    end_1_5_rotation()
  print("Paused End of World 1-5 macro")

def end_1_5_rotation():
  rng = random.random()
  gale_barrier()
  if should_pause(): return
  if not sphere():
    if should_pause(): return
    if not monsoon():
      if should_pause(): return
      howling_gale()
  if should_pause(): return
  if should_pause(): return
  if not merciless_winds():
    phalanx_charge()
  if should_pause(): return
  web()
  if rng > 0.5:
    b.press_release('d', 0.6)
  if should_pause(): return
  if datetime.now() > data['next_loot']:
    end_1_5_looting()
  else:
    # Hold hurricane for 3 seconds at least
    b.press('a')
    time.sleep(1)
    if should_pause(): return
    time.sleep(1)
    if should_pause(): return
    time.sleep(1)
    if should_pause(): return
    
    # Find mob before continuing
    count = 0
    mob_loc = None
    while mob_loc == None:
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8, grayscale=True, region=monster_region)
      time.sleep(0.3)
      count += 1
      if count > 20: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")
    if should_pause(): return
    b.release('a')
    if should_pause(): return

def end_1_5_looting():
  if datetime.now() > data['next_loot']:
    if should_pause(): return
    b.press('left')
    if should_pause(): return
    jump_attack(delayAfter=0.7)
    if should_pause(): return
    jump_attack(delayAfter=0.74)
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    b.release('left')
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    time.sleep(1.5)
    if should_pause(): return
    b.press('right')
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack(jumpDelay=0.3)
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    b.release('right')
    if should_pause(): return
    jump_up(jumpDelay=0.3, delayAfter=0.6)
    if should_pause(): return
    b.press_release('left')
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.6))
    # data['next_loot'] = datetime.now() + timedelta(minutes=0.2)

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('f4')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def gale_barrier(delayAfter=0.8):
  if datetime.now() > data['next_gale_barrier']:
    b.press_release('e', delay=delayAfter)
    data['next_gale_barrier'] = datetime.now() + timedelta(seconds=90)
    return True
  return False  

def monsoon(delayAfter=1.1):
  if datetime.now() > data['next_monsoon']:
    b.press_release('r', delay=delayAfter)
    data['next_monsoon'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False  

def sphere(delayAfter=0.9):
  if datetime.now() > data['next_sphere']:
    b.press_release('y', delay=delayAfter)
    data['next_sphere'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False

def merciless_winds(delayAfter=0.7):
  if datetime.now() > data['next_merciless_wind']:
    b.press_release('f', delay=delayAfter)
    data['next_merciless_wind'] = datetime.now() + timedelta(seconds=10)
    return True
  return False

def howling_gale(delayAfter=0.9):
  if datetime.now() > data['next_howling']:
    b.press_release('t', delay=delayAfter)
    data['next_howling'] = datetime.now() + timedelta(seconds=5)
    return True
  return False

def phalanx_charge(delayAfter=0.8):
  if datetime.now() > data['next_phalanx_charge']:
    b.press_release('g', delay=delayAfter)
    data['next_phalanx_charge'] = datetime.now() + timedelta(seconds=30)
    return True
  return False

def web(delayAfter=0.6):
  if datetime.now() > data['next_web']:
    b.press_release('shift', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False
  
def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['is_changed_map'] and pause_if_change_map(Images.LIMINIA_ICON):
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

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('space', jumpDelay)
  b.press_release('space', delayAfter)

def jump_attack(attackDelay=0.05, jumpDelay=0.03, delayAfter=0.55):
  b.press_release('space', jumpDelay)
  b.press_release('space', attackDelay)
  b.press_release('d', delayAfter)

def jump_up(jumpDelay=0.2, delayAfter=1):
  b.press('up')
  b.press_release('space', jumpDelay)
  b.press_release('space')
  b.release('up', delayAfter)
  
def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('space', 0.15)
  b.release('space')
  b.release('down', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  b.press('down')
  b.press('space', attackDelay)
  b.press_release('d', delayAfter)
  b.release('space')
  b.release('down')

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press_release('space')
  b.press_release('space', delayAfter)

def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

main()
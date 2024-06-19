import time
import random
import threading
import pygame
import pyautogui as pag
from datetime import datetime, timedelta
import os
from base import BotBase, Images, Audio, KeyListener, post_status
import interception
import sys
from state import state
import common
from common import uniform

def getMap():
  maps = {
    # "cernium": Images.CERNIUM_ICON,
    # "odium": Images.ODIUM_ICON,
    "liminia": Images.LIMINIA_ICON,
    "arcus": Images.ARCUS_ICON,
    "default": Images.ARCUS_ICON
  }
  return maps[state['script']] if state['script'] in maps else maps['default']

monster_outlaw4_region = (850, 180, 1360-850, 315-180)
monster_1_5_region = (800, 0, 600, 300)

b = None
data = {
  'next_mistral_spring': datetime.now(),
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
  scripts = {
    "liminia": end_1_5_macro,
    "arcus": outlaw4_macro,
    "default": outlaw4_macro
  }
  
  config = {
    "user": "justin",
    "script": scripts[state['script']],
    "disable_extras": True,
  }
  b = BotBase(data, config, args=sys.argv, scripts=scripts)
  b.run()

def should_exit(func=None): # Use as a decorator or as a function by calling should_exit()
  def wrapper(*args, **kwargs):
    # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
    if state['checkmap'] and not data['whiteroomed'] and common.pause_if_whiteroom(pag, data, getMap()):
      data['whiteroomed'] = True
    if data['is_paused']:
      raise Exception("Stopping thread")
    if callable(func):
        return func(*args, **kwargs)
  if callable(func):
    return wrapper
  return wrapper()

def check():
    b.check_rune()
    b.check_fam_leveling(fam_menu_key='f11', summon_fam_key='u')
    b.check_tof(",")
    b.check_wap()
    # b.check_elite_box()
    b.check_fam_fuel()

def outlaw4_macro():
  cycles = 1
  def loot():
    nonlocal cycles
    calibrate = cycles % 3 == 0
    data['next_loot'] = datetime.now() - timedelta(minutes=uniform(1.4, 1.6))
    if datetime.now() > data['next_erda_fountain']:
      # Erda Fountain
      b.press_release('left')
      flash_jump(jumpDelay=0.2, delayAfter=0.1)
      glide()
      time.sleep(0.2)
      b.press('left')
      time.sleep(0.6)
      b.release('left')
      erda_fountain()
      jump_down_attack(delayAfter=0.35)
      jump_down_attack(delayAfter=0.7)
      b.press('right')
      b.release('right')
      jump_attack()
      jump_attack()
      jump_attack()
      jump_attack()
      jump_attack()
      if calibrate:
        jump_attack()
        jump_attack()
      time.sleep(0.1)
      b.press_release('left')
      jump_up(delayAfter=0.4)
      if calibrate:
        glide(delayAfter=0, delayInBetween=0)
        glide(delayAfter=0, delayInBetween=0)
        glide()
        time.sleep(0.5)
      else:
        cape()
      flash_jump(delayAfter=0.03)
      glide(delayAfter=0, delayInBetween=0)
      glide(delayAfter=0, delayInBetween=0)
      glide()
      glide(delayAfter=0, delayInBetween=0)
      glide(delayAfter=0, delayInBetween=0)
      glide()
      glide(delayAfter=0, delayInBetween=0)
      glide(delayAfter=0, delayInBetween=0)
      glide()
      time.sleep(0.2)
      jump_down_attack(delayAfter=0.5)
      jump_attack(delayAfter=0.7)
      if calibrate:
        b.press('left')
        time.sleep(0.3)
        b.release('left')
      b.press_release('right')
      cycles += 1

  def rotation():
    rng = random.random()
    gale_barrier()
    if not sphere():
      if not monsoon():
        if not mistral_spring():
          howling_gale()
    else:
      merciless_winds()
    phalanx_charge(press_twice=True)
    web()
    if rng > 0.5:
      cape()

    if datetime.now() > data['next_erda_fountain']:
      time.sleep(0.2)
      loot()
    else:
      # b.press('a')
      time.sleep(1)
      should_exit()
      time.sleep(1)
      should_exit()
      time.sleep(1)
      should_exit()
      time.sleep(1)
      should_exit()

      # Find mob before continuing
      count = 0
      mob_loc = None
      while mob_loc == None:
        mob_loc = pag.locateOnScreen(Images.IRONSHOT1, confidence=0.9, grayscale=True, region=monster_outlaw4_region) or pag.locateOnScreen(Images.IRONSHOT2, confidence=0.9, grayscale=True, region=monster_outlaw4_region)
        time.sleep(0.3)
        count += 1
        if count > 20: break
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")
      should_exit()
      # b.release('a')
      should_exit()
  
  print("Started Outlaw Infested Waste 4 macro")
  while not should_exit():
    check()
    rotation()
  print("Paused Outlaw Infested Waste 4 macro")
  
def end_1_5_macro():
  print("Started End of World 1-5 macro")
  while not should_exit():
    check()
    end_1_5_rotation()
    end_1_5_looting()
  print("Paused End of World 1-5 macro")

def end_1_5_rotation():
  rng = random.random()
  gale_barrier()
  if not sphere():
    if not monsoon():
      howling_gale()
  if not merciless_winds():
    phalanx_charge()
  web()
  if rng > 0.5:
    cape()
  if datetime.now() > data['next_loot']:
    end_1_5_looting()
  else:
    # Hold hurricane for 3 seconds at least
    b.press('a')
    should_exit()
    time.sleep(1)
    should_exit()
    time.sleep(1)
    should_exit()
    time.sleep(1)
    
    # Find mob before continuing
    count = 0
    mob_loc = None
    while mob_loc == None:
      mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8, grayscale=True, region=monster_outlaw4_region)
      time.sleep(0.3)
      count += 1
      if count > 20: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")
    b.release('a')

def end_1_5_looting():
  if datetime.now() > data['next_loot']:
    b.press('left')
    jump_attack(delayAfter=0.7)
    jump_attack(delayAfter=0.74)
    jump_attack()
    b.release('left')
    erda_fountain()
    time.sleep(1.5)
    b.press('right')
    jump_attack()
    jump_attack(jumpDelay=0.45)
    jump_attack()
    jump_attack()
    b.release('right')
    jump_up(jumpDelay=0.35, delayAfter=0.6)
    b.press_release('left')
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.6))
    # data['next_loot'] = datetime.now() + timedelta(minutes=0.2)

@should_exit
def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('9')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

@should_exit
def cape(delayAfter=0.6):
  b.press_release('d', delayAfter)

@should_exit
def glide(delayAfter=0.52, delayInBetween=0.05):
  b.press_release('s', delay=delayAfter, delayInBetween=delayInBetween)

@should_exit
def mistral_spring(delayAfter=4):
  if datetime.now() > data['next_mistral_spring']:
    b.press_release('4', delay=delayAfter)
    data['next_mistral_spring'] = datetime.now() + timedelta(seconds=360)
    return True
  return False      

@should_exit
def gale_barrier(delayAfter=0.8):
  if datetime.now() > data['next_gale_barrier']:
    b.press_release('q', delay=delayAfter)
    data['next_gale_barrier'] = datetime.now() + timedelta(seconds=90)
    return True
  return False  

@should_exit
def monsoon(delayAfter=1.2):
  if datetime.now() > data['next_monsoon']:
    b.press_release('r', delay=delayAfter)
    data['next_monsoon'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False  

@should_exit
def sphere(delayAfter=0.9):
  if datetime.now() > data['next_sphere']:
    b.press_release('y', delay=delayAfter)
    data['next_sphere'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False

@should_exit
def merciless_winds(delayAfter=0.7):
  if datetime.now() > data['next_merciless_wind']:
    b.press_release('f', delay=delayAfter)
    data['next_merciless_wind'] = datetime.now() + timedelta(seconds=10)
    return True
  return False

@should_exit
def howling_gale(delayAfter=0.9):
  if datetime.now() > data['next_howling']:
    b.press_release('t', delay=delayAfter)
    data['next_howling'] = datetime.now() + timedelta(seconds=5)
    return True
  return False

@should_exit
def phalanx_charge(delayAfter=0.8, press_twice=False):
  if datetime.now() > data['next_phalanx_charge']:
    b.press_release('g', 0.2)
    if press_twice:
      b.press_release('g', 0.05)
    else:
      time.sleep(delayAfter)
    data['next_phalanx_charge'] = datetime.now() + timedelta(seconds=30)
    return True
  return False

@should_exit
def web(delayAfter=0.6):
  if datetime.now() > data['next_web']:
    b.press_release('shift', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False

@should_exit
def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('space', jumpDelay)
  b.press_release('space', delayAfter)

@should_exit
def jump_attack(attackDelay=0.05, jumpDelay=0.03, delayAfter=0.55):
  b.press_release('space', jumpDelay)
  b.press_release('space', attackDelay)
  b.press_release('d', delayAfter)

@should_exit
def jump_up(jumpDelay=0.2, delayAfter=1):
  b.press('up')
  b.press_release('space', jumpDelay)
  b.press_release('space')
  b.release('up', delayAfter)
  
@should_exit
def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('space', 0.15)
  b.release('space')
  b.release('down', delayAfter)

@should_exit
def jump_down_attack(attackDelay=0.05, delayAfter=1):
  b.press('down')
  b.press('space', attackDelay)
  b.press_release('d', delayAfter)
  b.release('space')
  b.release('down')

@should_exit
def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press_release('space')
  b.press_release('space', delayAfter)

main()
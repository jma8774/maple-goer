import time
import threading
import pygame
import pyautogui as pag
from datetime import datetime, timedelta
import os
from base import BotBase, Images, Audio, KeyListener, post_status
from state import state
import sys
import common
from common import uniform

monster_pinedeer_region = (17, 428, 524-17, 559-428)
monster_befuddle_region = (0, 450, 771-0, 581-450)

def getMap():
  maps = {
    "reverse": Images.REVERSE_ICON,
    "chuchu": Images.CHUCHU_ICON,
    # "arcana": Images.ARCANA_ICON,
    "default": Images.REVERSE_ICON
  }
  return maps[state['script']] if state['script'] in maps else maps['default']

b = None
data = {
  'next_erda_fountain': datetime.now(),
  'next_petfood': datetime.now() + timedelta(seconds=60),
  'next_falcon' : datetime.now(),
  'next_instant': datetime.now(),
  'next_summer': datetime.now(),
  'next_susanno': datetime.now(),
  'next_moon': datetime.now(),
}

def main():
  global b

  scripts = {
    "reverse": reverse_macro,
    "chuchu": chuchu_macro,
    # "arcana": arcana_macro,
    "default": reverse_macro,
  }

  config = {
    "user": "idk",
    "script": scripts[state['script']],
    "setup": setup,
    "disable_extras": True, 
  }
  b = BotBase(data, config, args=sys.argv, scripts=scripts)
  b.run()

def setup():
  pass

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
    now = datetime.now()
    b.check_rune()
    # b.check_fam_leveling(fam_menu_key='f11', summon_fam_key='u')
    # b.check_tof(",")
    # b.check_wap()
    # b.check_elite_box()
    # b.check_fam_fuel()
    if now > data['next_petfood']:
      b.press_release('f12')
      data['next_petfood'] = now + timedelta(seconds=60)
    # if now > data['next_manapot']:
    #   b.press_release('pageup')
    #   data['next_manapot'] = now + timedelta(seconds=22)

def arcana_macro():
  def loot():
    if datetime.now() > data['next_loot']:
      resistance()
      jump_attack()
      jump_attack()
      jump_attack(delayAfter=1)
      b.press_release('right')
      turret()
      mech_dash()
      lightning_bot()
      mech_jump("right")
      lightning_bot()
      mech_jump("right")
      lightning_bot()
      b.press('right', delay=0.2)
      b.release('right')
      mech_dash(delayAfter=0.8)
      jump_down_attack(jumpDelay=0.1, delayAfter=0.95)
      erda_fountain()
      b.press_release('left')
      mech_jump("left")
      bots()
      b.press('left', 0.4)
      b.release('left')
      mech_jump("left")
      data['next_loot'] = datetime.now() + timedelta(seconds=42)

  def rotation():
    # Find mob before continuing
    if state['scanmob']:
      count = 0
      mob_loc = None
      while mob_loc == None:
        mob_loc = pag.locateOnScreen(Images.BEFUDDLE1, confidence=0.9, grayscale=True, region=monster_befuddle_region) or pag.locateOnScreen(Images.BEFUDDLE2, confidence=0.9, grayscale=True, region=monster_befuddle_region)
        time.sleep(0.3)
        count += 1
        if count > 20: break
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")

    battery()
    shoot()
    b.press_release('right')
    missles()
    shoot()
    b.press_release('left')
    missles()
    
    
  print("Started Arcana macro")
  while not should_exit():
    check()
    rotation()
    loot()
  print("Paused Arcana macro")

def chuchu_macro():
  def rotation():
    wait = 7
    if not instant():
      if not summer():
        if not moon():
          falcon()
          phantom_blade()
          b.press_release('left')
          phantom_blade()
          b.press_release('right')
          wait = 5.5
        else:
          wait = 3.5
      else:
        wait = 4
    else:
      wait = 6.5
    if not erda_fountain():
      susanno()
    time.sleep(wait/4)
    should_exit()
    time.sleep(wait/4)
    should_exit()
    time.sleep(wait/4)
    should_exit()
    time.sleep(wait/4)
    should_exit()
          
  print("Started ChuChu macro")
  while not should_exit():
    check()
    rotation()
  print("Paused ChuChu macro")
  
def reverse_macro():
  def rotation():
    wait = 7
    if not instant():
      if not summer():
        if not moon():
          falcon()
          phantom_blade()
          b.press_release('left')
          phantom_blade()
          b.press_release('right')
          wait = 5.5
        else:
          wait = 3.5
      else:
        wait = 4
    else:
      wait = 6.5
    if datetime.now() > data['next_erda_fountain']:
      susanno()
      jump_down_attack()
      jump_attack()
      jump_attack()
      jump_attack()
      vapor()
      b.press_release('left')
      erda_fountain()
      jump_down_attack()
      jump_attack()
      jump_attack()
      jump_attack()
      vapor()
    else:
      time.sleep(wait/4)
      should_exit()
      time.sleep(wait/4)
      should_exit()
      time.sleep(wait/4)
      should_exit()
      time.sleep(wait/4)
      should_exit()
          
  print("Started Reverse macro")
  while not should_exit():
    check()
    rotation()
  print("Paused Reverse macro")

@should_exit
def missles():
    b.press_release('c')

@should_exit
def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press_release('b', delay=1)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

@should_exit
def falcon():
  if datetime.now() > data['next_falcon']:
    b.press_release('r', delay=0.7)
    data['next_falcon'] = datetime.now() + timedelta(seconds=8)
    return True
  return False

@should_exit
def instant():
  if datetime.now() > data['next_instant']:
    b.press_release('w', delay=0.6)
    data['next_instant'] = datetime.now() + timedelta(seconds=10)
    return True
  return False

@should_exit
def summer():
  if datetime.now() > data['next_summer']:
    b.press_release('4', delay=3)
    data['next_summer'] = datetime.now() + timedelta(seconds=120)
    return True
  return False

@should_exit
def susanno():
  if datetime.now() > data['next_susanno']:
    b.press_release('3', delay=0.7)
    data['next_susanno'] = datetime.now() + timedelta(seconds=120)
    return True
  return False
  
@should_exit
def moon():
  if datetime.now() > data['next_moon']:
    b.press_release('1', delay=3.5)
    data['next_moon'] = datetime.now() + timedelta(seconds=90)
    return True
  return False

@should_exit
def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('e', jumpDelay)
  b.press_release('e', delayAfter)

@should_exit
def jump_attack(attackDelay=0.05, jumpDelay=0.03, delayAfter=0.58):
  b.press_release('e', jumpDelay)
  b.press_release('e', attackDelay)
  b.press_release('q', delayAfter)

@should_exit
def jump_up(jumpDelay=0.2, delayAfter=1):
  b.press('up')
  b.press_release('e', jumpDelay)
  b.press_release('e')
  b.release('up', delayAfter)
  
@should_exit
def jump_down(delayAfter=1):
  b.press('down', 0.15)
  b.press('e', 0.15)
  b.release('e')
  b.release('down', delayAfter)

@should_exit
def jump_down_attack(jumpDelay=0.05, attackDelay=0.05, delayAfter=1):
  b.press('down', jumpDelay)
  b.press('e', attackDelay)
  b.press_release('q', delayAfter)
  b.release('e')
  b.release('down')

@should_exit
def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press_release('e')
  b.press_release('e', delayAfter)

@should_exit
def shoot(delayAfter=0.7):
  b.press_release('q', delayAfter)

@should_exit
def phantom_blade(delayAfter=0.7):
  b.press_release('2', delayAfter)

@should_exit
def vapor(delayAfter=1.2):
  b.press_release('c', delayAfter)


main()
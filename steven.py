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
    "chuchu": Images.CHUCHU_ICON,
    "arcana": Images.ARCANA_ICON,
    "default": Images.ARCANA_ICON
  }
  return maps[state['script']] if state['script'] in maps else maps['default']

b = None
data = {
  'next_erda_fountain': datetime.now(),
  'next_doomsday': datetime.now(),
  'next_carrier': datetime.now(),
  'next_petfood': datetime.now() + timedelta(seconds=60),
  'next_heal': datetime.now(),
  'next_dice': datetime.now(),
  'next_manapot': datetime.now() + timedelta(seconds=60),
  'next_resistance': datetime.now(),
  'next_battery': datetime.now(),
}

def main():
  global b

  scripts = {
    "chuchu": chuchu_macro,
    "arcana": arcana_macro,
    "default": arcana_macro,
  }

  config = {
    "user": "steven",
    "script": scripts[state['script']],
    "setup": setup,
    "disable_extras": True, 
  }
  b = BotBase(data, config, args=sys.argv, scripts=scripts)
  b.run()

def setup():
  data['next_loot'] = datetime.now() - timedelta(seconds=10)

def should_exit(func=None): # Use as a decorator or as a function by calling should_exit()
  def wrapper(*args, **kwargs):
    # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
    if state['checkmap'] and not data['whiteroomed'] and common.pause_if_whiteroom(pag, data, getMap()):
      data['whiteroomed'] = True
    if data['is_paused']:
      raise Exception("Stopping thread")
    if callable(func):
        func(*args, **kwargs)
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
    # if now > data['next_petfood']:
    #   b.press_release('home')
    #   data['next_petfood'] = now + timedelta(seconds=60)
    # if now > data['next_manapot']:
    #   b.press_release('pageup')
    #   data['next_manapot'] = now + timedelta(seconds=22)
    healbot()
    dice()
    carrier()
    doomsday()

def arcana_macro():
  def loot():
    if datetime.now() > data['next_loot']:
      resistance()
      jump_attack()
      jump_attack()
      b.press_release('right')
      time.sleep(0.3)
      jump_attack(delayAfter=1)
      turret()
      mech_dash()
      lightning_bot()
      mech_jump("right")
      lightning_bot()
      mech_jump("right")
      lightning_bot()
      mech_dash(delayAfter=0.8)
      jump_down_attack(jumpDelay=0.1, delayAfter=0.9)
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
  data['last_wipe'] = datetime.now()
  def loot():
    if datetime.now() > data['next_loot']:
      resistance()
      b.press_release("right")
      jump_attack()
      jump_attack()
      bots()
      mech_jump("right")
      erda_fountain()
      jump_attack()
      b.press_release('x', 1)
      b.press('left', 0.3)
      jump_attack()
      jump_attack()
      b.release('left')
      turret()
      mech_jump("left")
      lightning_bot()
      missles()
      mech_dash()
      mech_dash()
      lightning_bot()
      missles()
      mech_jump("left")
      lightning_bot()
      missles()
      jump_attack()
      b.press_release('right')
      jump_down(delayAfter=0.1)
      jump_down(delayAfter=1.4)
      jump_attack()
      jump_attack()
      mech_jump("right", dashDelay=0.2)
      data['next_loot'] = datetime.now() + timedelta(seconds=40)

  def rotation():
    while datetime.now() - data['last_wipe'] < timedelta(seconds=3):
      time.sleep(0.5)

    # Find mob before continuing
    if state['scanmob']:
      count = 0
      mob_loc = None
      while mob_loc == None:
        mob_loc = pag.locateOnScreen(Images.PINEDEER1, confidence=0.9, grayscale=True, region=monster_pinedeer_region) or pag.locateOnScreen(Images.PINEDEER2, confidence=0.9, grayscale=True, region=monster_pinedeer_region)
        time.sleep(0.3)
        count += 1
        if count > 20: break
      if mob_loc == None:
        print(f"Couldn't find mob after {count} tries, continuing rotation")
      else:
        print(f"Found mob at {mob_loc}, continuing rotation")

    battery()
    shoot()
    b.press_release('left')
    missles()
    shoot()
    b.press_release('right')
    missles()
    data['last_wipe'] = datetime.now()
  
  print("Started ChuChu macro")
  while not should_exit():
    check()
    rotation()
    loot()
  print("Paused ChuChu macro")
  
@should_exit
def missles():
    b.press_release('c')

@should_exit
def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press_release('y', delay=1)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

@should_exit
def doomsday():
  if datetime.now() > data['next_doomsday']:
    b.press_release('w', 0.8)
    data['next_doomsday'] = datetime.now() + timedelta(seconds=181)
    return True
  return False

@should_exit
def battery():
  if datetime.now() > data['next_battery']:
    b.press_release('s', 0.8)
    data['next_battery'] = datetime.now() + timedelta(seconds=25)
    return True
  return False

@should_exit
def healbot():
  if datetime.now() > data['next_heal']:
    b.press_release('q', 0.8)
    data['next_heal'] = datetime.now() + timedelta(seconds=80)
    return True
  return False

@should_exit
def dice():
  if datetime.now() > data['next_dice']:
    b.press_release('1', 0.8)
    data['next_dice'] = datetime.now() + timedelta(seconds=202)
    return True
  return False
  
@should_exit
def resistance():
  if datetime.now() > data['next_resistance']:
    b.press_release('d', 0.8)
    data['next_resistance'] = datetime.now() + timedelta(seconds=25)
    return True
  return False

@should_exit
def carrier():
  if datetime.now() > data['next_carrier']:
    b.press_release('e', 0.8)
    data['next_carrier'] = datetime.now() + timedelta(seconds=181)
    return True
  return False
 
@should_exit
def bots():
  b.press_release('f', 0.7)

@should_exit
def turret():
  b.press_release('g', 0.7)

@should_exit
def lightning_bot():
  b.press_release('h', 0.7)

@should_exit
def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  b.press_release('space', jumpDelay)
  b.press_release('space', delayAfter)

@should_exit
def mech_dash(delayAfter=0.5):
  b.press_release('z', delayAfter)

@should_exit
def mech_jump(direction, jumpDelay=0.1, dashDelay=0.3, delayAfter=1.1):
  b.press_release('space', jumpDelay)
  b.press_release('space', dashDelay)
  b.press(direction, 0.02)
  b.press_release('z', 0.02)
  b.release(direction, delayAfter)

@should_exit
def jump_attack(attackDelay=0.05, jumpDelay=0.03, delayAfter=0.58):
  b.press_release('space', jumpDelay)
  b.press_release('space', attackDelay)
  b.press_release('v', delayAfter)

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
def jump_down_attack(jumpDelay=0.05, attackDelay=0.05, delayAfter=1):
  b.press('down', jumpDelay)
  b.press('space', attackDelay)
  b.press_release('v', delayAfter)
  b.release('space')
  b.release('down')

@should_exit
def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  b.press_release('space')
  b.press_release('space', delayAfter)

@should_exit
def shoot(delayAfter=0.7):
  b.press_release('v', delayAfter)

main()
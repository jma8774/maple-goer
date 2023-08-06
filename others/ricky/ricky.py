import time
import keyboard
import random
import threading
from datetime import datetime, timedelta
import pyautogui as pag
from PIL import Image

def openImage(file):
  return Image.open(f"images/{file}")

class Images:
  FOREBERION      = openImage('foreberion.png')

START_KEY = 'f7'
PAUSE_KEY = 'f8'

logging = False
thread = None
data = {
  'is_paused': True,
  'next_loot': datetime.now() + timedelta(minutes=1.5),

  'next_fire_floor': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_fire_breath': datetime.now(),
  'next_dark_fog': datetime.now(),
  'next_onyx_dragon': datetime.now(),
  'next_web': datetime.now(),
}

def main():
  commands()
  keyboard.add_hotkey(PAUSE_KEY, pause)
  keyboard.add_hotkey(START_KEY, start)
  while True:
    keyboard.read_key()
    if data['is_paused'] == True:
      continue
    thread = threading.Thread(target=liminia_1_5_macro)
    thread.start()
    thread.join()
    release_all()

def liminia_1_5_macro():
  print("Starting 1-5 macro")
  while not data['is_paused']:
    liminia_1_5_rotation()
    release_all()

def liminia_1_5_rotation():
  # Find mob before starting rotation
  start_wait = datetime.now()
  mob_loc = pag.locateOnScreen(Images.FOREBERION, confidence=0.8)
  while mob_loc == None:
    if data['is_paused']: return
    mob_loc = pag.locateOnScreen(Images.FOREBERION, confidence=0.8)
    time.sleep(0.5)
    if datetime.now() - start_wait > timedelta(seconds=7):
      break
  if mob_loc == None:
    print(f"Couldn't find mob after 7 secs, continuing rotation")
  else:
    print(f"Found mob at {mob_loc}, continuing rotation")

  if datetime.now() > data['next_fire_breath']:
    fire_breath()
    if datetime.now() > data['next_fire_floor']:
      press('left')
      if data['is_paused']: return
      teleport()
      if data['is_paused']: return
      teleport()
      if data['is_paused']: return
      teleport()
      if data['is_paused']: return
      press_release('ctrl')
      if data['is_paused']: return
      release('left')
      if data['is_paused']: return
      if datetime.now() > data['next_erda_fountain']:
        press('left')
        teleport()
        if data['is_paused']: return
        release('left')
        if data['is_paused']: return
        erda_fountain()
        press('right')
        teleport()
        if data['is_paused']: return
        teleport()
        teleport()
        if data['is_paused']: return
        teleport()
        if data['is_paused']: return
        teleport()
        if data['is_paused']: return
        release('right')
        press_release('left')
        if data['is_paused']: return
      else:
        press('right')
        if data['is_paused']: return
        teleport()
        teleport()
        if data['is_paused']: return
        teleport()
        teleport()
        if data['is_paused']: return
        release('right')
        if data['is_paused']: return
        press_release('left')
        if data['is_paused']: return
      data['next_fire_floor'] = datetime.now() + timedelta(seconds=uniform(15, 20))
    else:
      if not liminia_1_5_loot():
        dark_fog()
        time.sleep(5)
      if data['is_paused']: return
  else:
    wind_breath()
    if not liminia_1_5_loot():
      dark_fog()
      time.sleep(5)
    if data['is_paused']: return

def liminia_1_5_loot():
  if datetime.now() < data['next_loot']:
    return
  if data['is_paused']: return
  press('up')
  if data['is_paused']: return
  teleport()
  if data['is_paused']: return
  release('up')
  if data['is_paused']: return
  press('left', 2)
  if data['is_paused']: return
  release('left')

  # Use spider web or onyx on top
  if not summon_web():
    if datetime.now() > data['next_onyx_dragon']:
      press('up')
      teleport()
      release('up')
      summon_onyx()
      press('down')
      teleport()
      release('down')

  if data['is_paused']: return
  press('down')
  if data['is_paused']: return
  teleport()
  release('down')
  # jump_down(delayAfter=2)
  # if data['is_paused']: return
  # jump_down(delayAfter=1.5)
  # if data['is_paused']: return
  # press('left')
  # if data['is_paused']: return
  # teleport()
  # if data['is_paused']: return
  # release('left')
  # if data['is_paused']: return
  # press('right')
  # if data['is_paused']: return
  # teleport()
  # if data['is_paused']: return
  # release('right')
  # if data['is_paused']: return
  # jump_down(0.5)
  # if data['is_paused']: return
  # press('down')
  # if data['is_paused']: return
  # teleport()
  # if data['is_paused']: return
  # release('down')
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  teleport()
  if data['is_paused']: return
  teleport()
  # # if data['is_paused']: return
  # # teleport()
  if data['is_paused']: return
  release('right')
  if data['is_paused']: return
  press_release('left')
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.3, 1.7))
  return True

def dark_fog():
  if datetime.now() < data['next_dark_fog']:
    return
  press_release('page down', 0.6)
  data['next_dark_fog'] = datetime.now() + timedelta(seconds=uniform(40, 50))
  
def fire_breath():
  press_release('g')
  press_release('t', 0.7)
  data['next_fire_breath'] = datetime.now() + timedelta(seconds=10)

def wind_breath():
  press_release('a')
  press_release('f', 0.7)

def summon_onyx():
  if datetime.now() > data['next_onyx_dragon']:
    press_release('4')
    press_release('4', 0.8)
    data['next_onyx_dragon'] = datetime.now() + timedelta(seconds=80)
    return True
  return False

def summon_web():
  if datetime.now() > data['next_web']:
    press_release('delete')
    press_release('delete', 0.8)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False

def teleport():
  press_release('d', 0.65)

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    press('down')
    press_release('x')
    press_release('x')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)

def jump_up(delayAfter=1):
  press('up')
  press_release('w', 0.2)
  press_release('w')
  press_release('w')
  release('up')
  time.sleep(delayAfter)

def jump_down(delayAfter=1):
  if logging:
    print('jump_down')
  press('down', 0.15)
  press('w')
  time.sleep(0.15)
  release('w')
  release('down')
  time.sleep(delayAfter)

def pause():
  print('Pause')
  data['is_paused'] = True
  data['x_and_down_x'] = True

def start():
  print('Start')
  data['is_paused'] = False

def release_all():
  if keyboard.is_pressed('left'):
    release('left', delay=0.05)
  if keyboard.is_pressed('right'):
    release('right', delay=0.05)
  if keyboard.is_pressed('up'):
    release('up', delay=0.05)
  if keyboard.is_pressed('down'):
    release('down', delay=0.05)
  if keyboard.is_pressed('ctrl'):
    release('ctrl', delay=0.05)
  if keyboard.is_pressed('alt'):
    release('alt', delay=0.05)
  if keyboard.is_pressed('f7'):
    release('f7', delay=0.05)
  if keyboard.is_pressed('f8'):
    release('f8', delay=0.05)

def press(key, delay=0.05):
  keyboard.press(key)
  time.sleep(delay)
  
def release(key, delay=0.05):
  keyboard.release(key)
  time.sleep(delay)

def send(key, delay=0.05):
  keyboard.send(key)
  time.sleep(delay)

def press_release(key, delay=0.05):
  if logging:
    print(f"press_release({key})")
  keyboard.press(key)
  time.sleep(0.05)
  keyboard.release(key)
  time.sleep(delay)
  
def write(word, delay=0.05):
  keyboard.write(word)
  time.sleep(delay)

def uniform(a, b):
  return random.uniform(a, b)

def commands():
  print("Commands:")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")

main()
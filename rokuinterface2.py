import time
import keyboard
import random
import threading
from datetime import datetime, timedelta

START_KEY = 'f7'
PAUSE_KEY = 'f8'

logging = False
thread = None
data = {
  'is_paused': True,
  'next_loot': datetime.now() + timedelta(minutes=1.7),
  'next_monsoon': datetime.now(),
  'next_sphere': datetime.now(),
  'next_merciless_wind': datetime.now(),
  'next_howling': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_pot': datetime.now(),
}

def main():
  commands()
  keyboard.add_hotkey(PAUSE_KEY, pause)
  keyboard.add_hotkey(START_KEY, start)
  while True:
    keyboard.wait(START_KEY)
    thread = threading.Thread(target=lh6_macro)
    thread.start()
    thread.join()
    release_all()

def lh6_macro():
  print("Starting Last Horizon 6 macro")
  while not data['is_paused']:
    lh6_rotation()
    # lh6_loot()

def lh6_rotation():
  rng = random.random()
  press_release('right')
  if datetime.now() > data['next_sphere']:
    if data['is_paused']: return
    sphere(delayAfter=0.8)
  else:
    if data['is_paused']: return
    howling_gale(delayAfter=0.8)

  if rng < 0.3:
    if data['is_paused']: return
    press('right', 1.15)
    if data['is_paused']: return
    release('right', 0.05)
  elif rng > 0.3 and rng < 0.6:
    if data['is_paused']: return
    press('right')
    if data['is_paused']: return
    press_release('space', 1.1)
    if data['is_paused']: return
    release('right', 0.05)
  else:
    if data['is_paused']: return
    press_release('s', 0.5)
    if data['is_paused']: return
    press('left', 0.2)
    release('left')
    if data['is_paused']: return
    press_release('right')
  if data['is_paused']: return
  press_release('up')
  if data['is_paused']: return
  press_release('up', 0.5)

  if data['is_paused']: return
  jump_down_attack(attackDelay=0.4, delayAfter=0.45)
  if data['is_paused']: return
  press('right', delay=0.3)
  if data['is_paused']: return
  jump_attack(delayAfter=0.6)
  if data['is_paused']: return
  jump_attack(delayAfter=0.6)
  if data['is_paused']: return
  jump_attack(delayAfter=0.6)
  just_used_fountain = False
  if datetime.now() > data['next_erda_fountain']:
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    release('right')
    if data['is_paused']: return
    press('left', 0.3)
    if data['is_paused']: return
    release('left')
    if data['is_paused']: return
    erda_fountain()
    just_used_fountain = True
  release('right')

  rng = random.random()
  if just_used_fountain:
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    flash_jump(delayAfter=0.55)
    if data['is_paused']: return
    press_release('left', 1.2)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
  elif rng > 0.5:
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    jump_down_attack(attackDelay=0.4, delayAfter=0.05)
    if data['is_paused']: return
    time.sleep(0.4)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    flash_jump(jumpDelay=uniform(0.33, 0.4), delayAfter=0.7)
    if data['is_paused']: return
    jump_down_attack(attackDelay=0.4, delayAfter=0.4)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
  else:
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)
    if data['is_paused']: return
    jump_down_attack(attackDelay=0.4, delayAfter=0.4)
    if data['is_paused']: return
    jump_down_attack(attackDelay=0.4, delayAfter=0.4)
    if data['is_paused']: return
    jump_attack(delayAfter=0.6)

def lh6_loot():
  if False and datetime.now() < data['next_loot']:
    return
  rng = random.random()
  press_release('right')
  if rng < 0.3:
    press('right', 1.15)
    release('right', 0.05)
  elif rng > 0.3 and rng < 0.6:
    press('right')
    press_release('space', 1.1)
    release('right', 0.05)
  else:
    press_release('s', 0.5)
    press('left', 0.2)
    release('left')
    press_release('right')
  press_release('up')
  press_release('up', 0.5)
  press_release('right')
  jump_attack(delayAfter=0.6)
  jump_attack(delayAfter=0.6)
  jump_attack(delayAfter=0.6)
  jump_attack(delayAfter=0.6)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 1.9))

def buff():
  pass

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    press('down')
    press_release('f4')
    press_release('f4')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)

def monsoon(delayAfter=0.3):
  press_release('r', delay=delayAfter)
  data['next_monsoon'] = datetime.now() + timedelta(seconds=30)

def sphere(delayAfter=0.3):
  press_release('y', delay=delayAfter)
  data['next_sphere'] = datetime.now() + timedelta(seconds=30)

def merciless_winds(delayAfter=0.3):
  press_release('f', delay=delayAfter)
  data['next_merciless_wind'] = datetime.now() + timedelta(seconds=10)

def howling_gale(delayAfter=0.3):
  press_release('t', delay=delayAfter)
  data['next_howling'] = datetime.now() + timedelta(seconds=10)
  
def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  press_release('space')
  time.sleep(jumpDelay)
  press_release('space')
  time.sleep(delayAfter)

def jump_attack(attackDelay=0.2, jumpDelay=0.05, delayAfter=0.7):
  press_release('space', jumpDelay)
  press_release('space', attackDelay)
  keyboard.send('d')
  time.sleep(delayAfter)

def jump_up(delayAfter=1):
  press('up')
  press_release('space', 0.2)
  press_release('space')
  press_release('space')
  release('up')
  time.sleep(delayAfter)
  
def jump_down(delayAfter=1):
  if logging:
    print('jump_down')
  press('down', 0.15)
  press('space')
  time.sleep(0.15)
  release('space')
  release('down')
  time.sleep(delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  if logging:
    print('jump_down_attack')
  press('down')
  press('space')
  time.sleep(attackDelay)
  press_release('d')
  time.sleep(delayAfter)
  release('space')
  release('down')

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  keyboard.press('space')
  time.sleep(0.05)
  keyboard.release('space')
  time.sleep(0.05)
  keyboard.press('space')
  time.sleep(0.05)
  keyboard.release('space')
  time.sleep(delayAfter)

def pause():
  print('Pause')
  data['is_paused'] = True
  data['x_and_down_x'] = True

def start():
  print('Start')
  data['is_paused'] = False

def release_all():
  release('left', delay=0.05)
  release('right', delay=0.05)
  release('space', delay=0.05)

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
  
def uniform(a, b):
  return random.uniform(a, b)

def commands():
  print("Commands:")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")

main()
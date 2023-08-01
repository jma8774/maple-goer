import time
import keyboard
import random
import threading
import sys
import pyautogui as pag
from datetime import datetime, timedelta
from marketplace import Images

JIAMING_KEY = 'f5'
JIAMING_PW_KEY = 'alt+f5'
JIMMY_KEY = 'f6'
JIMMY_PW_KEY = 'alt+f6'
START_KEY = 'f7'
PAUSE_KEY = 'f8'

logging = False
thread = None
data = {
  'is_paused': True,
  'next_sharpeye': datetime.now(),
  'next_split': datetime.now(),
  'current_split_ends_at': datetime.now(),
  'next_surgebolt': datetime.now(),

  'next_loot': datetime.now() + timedelta(minutes=1.5),
  'next_loot_2': datetime.now() + timedelta(minutes=1.2),
  'next_loot_3': datetime.now() + timedelta(minutes=1.2),

  'next_blink_setup': None,
  'next_web': datetime.now(),
  'next_bird': datetime.now(),
  'next_high_speed': datetime.now(),
  'x_and_down_x': False,

  'next_erda_fountain': datetime.now(),
  'next_bolt_burst': datetime.now(),
}

def main():
  commands()
  keyboard.add_hotkey(PAUSE_KEY, pause)
  keyboard.add_hotkey(START_KEY, start)
  keyboard.add_hotkey(JIAMING_KEY, writeJiamingEmail)
  keyboard.add_hotkey(JIAMING_PW_KEY, writeJiamingPw)
  keyboard.add_hotkey(JIMMY_KEY, writeJimmyEmail)
  keyboard.add_hotkey(JIMMY_PW_KEY, writeJimmyPw)
  while True:
    keyboard.read_key()
    if data['is_paused'] == True:
      continue
    data['next_blink_setup'] = None
    thread = threading.Thread(target=midpoint3_macro)
    thread.start()
    thread.join()
    release_all()

def midpoint3_macro():
  print("Starting World's Sorrow Midpoint 3 macro")
  while not data['is_paused']:
    buff()
    midpoint3_rotation()
    midpoint3_loot()
    release_all()

def midpoint3_rotation():
  mob_loc = None
  rng = random.random()
  if datetime.now() > data['next_erda_fountain']:
    if data['is_paused']: return
    press_release('shift', 1)
    press('right', 0.3)
    release('right')
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.5)
    if data['is_paused']: return
    erda_fountain()
    if data['is_paused']: return
    press_release('x')
    if data['is_paused']: return
    press_release('x', 0.7) 
  
  # Find mob before starting rotation
  start_wait = datetime.now()
  mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8)
  while mob_loc == None:
    if data['is_paused']: return
    mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8)
    time.sleep(0.5)
    if datetime.now() - start_wait > timedelta(seconds=9):
      break
  if mob_loc == None:
    print(f"Couldn't find mob after 9 secs, continuing rotation")
  else:
    print(f"Found mob at {mob_loc}, continuing rotation")

  if data['is_paused']: return
  jump_down_attack(delayAfter=0.55)
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.55)
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.65)
  if data['is_paused']: return
  press_release('right')
  if not high_speed_shot(0.8, rng > 0.8):
    q_and_surgebolt(afterDelay=0.63)

def midpoint3_loot():
  loot_variation = int(random.random() * 3)
  
  def face_left_teleport_reset():
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    press_release('left', 0.2)
    if data['is_paused']: return
    teleport_reset(0.7)

  if datetime.now() < data['next_loot']:
    face_left_teleport_reset()
    return
  
  rng = random.random()
  rng2 = random.random()
  def right_part():
    if data['is_paused']: return
    press_release('shift', 1)
    press('right', 0.3)
    release('right')
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    jump_down(delayAfter=0.1)
    if data['is_paused']: return
    if not bolt_burst(0.6, rng < 0.5):
      q_and_surgebolt(afterDelay=0.6)
    if data['is_paused']: return
    erda_fountain()
    if data['is_paused']: return
    jump_down_attack(delayAfter=1)
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.7)
    if data['is_paused']: return
    if not jump_high_speed_shot(delayAfter=0.5, isGo=rng2 > 0.5):
      jump_down_attack(delayAfter=0.5)
    press_release('right', 0.1)
    if data['is_paused']: return
    if not jump_web(delayAfter=1.5):
      if data['is_paused']: return
      jump_down_attack(delayAfter=1.5)
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    teleport_reset(0.7)

  def left_part():
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.5)
    if data['is_paused']: return
    press('left', 1.2)
    if data['is_paused']: return
    release('left', 0.5)
    press_release('right')
    if data['is_paused']: return
    if not jump_web(delayAfter=1):
      if data['is_paused']: return
      jump_down_attack(delayAfter=1)
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.7)
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.6)
    if data['is_paused']: return
    press_release('left')
    press_release('left')
    if data['is_paused']: return
    jump_down(delayAfter=0.1)
    if data['is_paused']: return
    if not bolt_burst(1.5, rng >= 0.5):
      if data['is_paused']: return
      q_and_surgebolt(afterDelay=1.5)
    if data['is_paused']: return
    teleport_reset(0.7)

  if loot_variation == 0:
    face_left_teleport_reset()
    right_part()
    left_part()
  elif loot_variation == 1:
    face_left_teleport_reset()
    left_part()
    right_part()
  else:
    press('left', 1.5)
    release('left', 0.7)
    press_release('c', 1.4)
    if not bolt_burst(0.7):
      q_and_surgebolt(afterDelay=0.7)
    press_release('right')
    jump_down_attack(delayAfter=0.55)
    press_release('left')
    jump_down_attack(delayAfter=0.7)
    teleport_reset(0.7)
    right_part()

  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.5, 1.7))

def buff():
  cur = datetime.now()
  if data['x_and_down_x']:
    press_release('x')
    press_release('x', 0.8)
    press('down')
    press_release('x')
    press_release('x')
    release('down')
    time.sleep(0.7)
    data['x_and_down_x'] = False
    data['next_blink_setup'] = datetime.now() + timedelta(seconds=uniform(40, 59))
  if cur > data['next_sharpeye']:
    data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(200, 300))
    press_release('page down', 2)
  if cur > data['next_split']:
    data['next_split'] = datetime.now() + timedelta(seconds=uniform(120, 140))
    data['current_split_ends_at'] = datetime.now() + timedelta(seconds=71)
    press_release('2', 1)
  if cur > data['next_bird']:
    press_release('5', 0.7)
    data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 125))
  if data['next_blink_setup'] == None:
    press_release('x')
    press_release('x', 0.7)
    data['next_blink_setup'] = datetime.now() + timedelta(seconds=uniform(40, 59))
  elif datetime.now() > data['next_blink_setup']:
    press('down')
    press_release('x')
    press_release('x')
    release('down')
    time.sleep(0.7)
    data['next_blink_setup'] = datetime.now() + timedelta(seconds=uniform(40, 59))
  
def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    press('down')
    press_release('f')
    press_release('f')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)

def bolt_burst(delayAfter=0.05, isGo=True):
  if isGo and datetime.now() > data['next_bolt_burst']:
    press_release('d', delay=delayAfter)
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
    press_release('4', delay=delayAfter)
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
    press_release('r', delay=delayAfter)
    data['next_high_speed'] = datetime.now() + timedelta(seconds=15)
    return True
  return False

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  press_release('alt')
  time.sleep(jumpDelay)
  press_release('alt')
  time.sleep(delayAfter)

def jump_attack(attackDelay=0.2, jumpDelay=0.05, delayAfter=0.7):
  rng = random.random()
  press_release('alt', jumpDelay)
  press_release('alt', attackDelay)
  keyboard.send('q')
  if rng > 0.7:
    send('e')
  time.sleep(delayAfter)

def jump_up(delayAfter=1):
  press('up')
  press_release('alt', 0.2)
  press_release('alt')
  press_release('alt')
  release('up')
  time.sleep(delayAfter)

def jump_down(delayAfter=1):
  if logging:
    print('jump_down')
  press('down', 0.15)
  press('alt')
  time.sleep(0.15)
  release('alt')
  release('down')
  time.sleep(delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  if logging:
    print('jump_down_attack')
  press('down')
  press('alt')
  time.sleep(attackDelay)
  press_release('q')
  release('alt')
  release('down')
  time.sleep(delayAfter)

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  keyboard.press('alt')
  time.sleep(0.05)
  keyboard.release('alt')
  time.sleep(0.05)
  keyboard.press('alt')
  time.sleep(0.05)
  keyboard.release('alt')
  time.sleep(delayAfter)

def q_and_surgebolt(afterDelay=0.7):
  if logging: 
    print('q_and_surgebolt')
  if datetime.now() > data['next_surgebolt']:
    press('q', delay=0.02)
    press_release('e')
    release('q')
    data['next_surgebolt'] = datetime.now() + timedelta(seconds=uniform(10, 13))
  else:
    press_release('q')
  time.sleep(afterDelay)

def teleport_reset(delayAfter=0.7):
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x', delayAfter)

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
  if keyboard.is_pressed('q'):
    release('q', delay=0.05)
  if keyboard.is_pressed('e'):
    release('e', delay=0.05)
  if keyboard.is_pressed('d'):
    release('d', delay=0.05)

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

def writeJimmyEmail():
  print('Writing jimmyma1991@gmail.com')
  write('jimmyma1991@gmail.com')

def writeJimmyPw():
  print('Writing PW')
  write('Aicilla1!!')

def writeJiamingEmail():
  print('Writing jiamingma1998@gmail.com')
  write('jiamingma1998@gmail.com')

def writeJiamingPw():
  print('Writing PW')
  write('Aicilla1!')

def uniform(a, b):
  return random.uniform(a, b)

def commands():
  print("Commands:")
  print(f"  {JIAMING_KEY} - write jiaming email")
  print(f"  {JIAMING_PW_KEY} - write jiaming pw")
  print(f"  {JIMMY_KEY} - write jimmy email")
  print(f"  {JIMMY_PW_KEY} - write jimmy pw")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")

if __name__=="__main__":
  main()
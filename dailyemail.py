import time
import keyboard
import random
import threading
import sys
from datetime import datetime, timedelta

TEAMVIEW_LEFT = 'f1'
TEAMVIEW_RIGHT = 'f2'
TEAMVIEW_JUMP_DOWN = 'f3'
TEAMVIEW_JUMP_UP = 'f4'

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
  'next_loot': datetime.now() + timedelta(minutes=1.2),
  'just_looted': datetime.now() + timedelta(seconds=5),
  'next_loot_2': datetime.now() + timedelta(minutes=1.2),
  'next_loot_3': datetime.now() + timedelta(minutes=1.2),
  'next_blink_setup': None,
  'next_web': datetime.now(),
  'next_feed_pet': datetime.now() + timedelta(minutes=1),
  'next_erda_fountain': datetime.now(),
  'next_bird': datetime.now(),
  'next_bolt_burst': datetime.now(),
  'x_and_down_x': False,

  'is_teamviewer_enabled': False,
}

def main():
  # Save commandline args
  for arg in sys.argv:
    data['is_teamviewer_enabled'] = data['is_teamviewer_enabled'] or arg == 'teamviewer' or arg == 'tv'

  # Register hotkeys for teamviewer if arg is specified
  if data['is_teamviewer_enabled']:
    tv = Teamviewer()
    keyboard.add_hotkey(TEAMVIEW_LEFT, tv.left)
    keyboard.add_hotkey(TEAMVIEW_RIGHT, tv.right)
    keyboard.add_hotkey(TEAMVIEW_JUMP_DOWN, tv.jump_down)
    keyboard.add_hotkey(TEAMVIEW_JUMP_UP, tv.jump_up)

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
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 2))
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

def midpoint3_rotation():
  if datetime.now() > data['next_erda_fountain']:
    if data['is_paused']: return
    press_release('shift', 1)
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.5)
    if data['is_paused']: return
    erda_fountain()
    if data['is_paused']: return
    press_release('x')
    if data['is_paused']: return
    press_release('x', 0.7) 
  elif datetime.now() > data['just_looted']:
    if data['is_paused']: return
    time.sleep(uniform(1, 3))
  if data['is_paused']: return
  jump_down_attack(delayAfter=0.55)
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.55)
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  press_release('left', 0.2)
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x')
  press_release('x', 0.7)

def midpoint3_loot():
  if datetime.now() < data['next_loot']:
    return
  rng = random.random()
  if data['is_paused']: return
  press_release('shift', 1)
  if data['is_paused']: return
  jump_down(delayAfter=0.1)
  if data['is_paused']: return
  if not bolt_burst(0.7, rng < 0.5):
    q_and_surgebolt(afterDelay=0.7)
  if data['is_paused']: return
  erda_fountain()
  if data['is_paused']: return
  jump_down_attack(delayAfter=1)
  if data['is_paused']: return
  jump_down_attack(delayAfter=1)
  if data['is_paused']: return
  jump_down_attack(delayAfter=0.6)
  press_release('right', 0.1)
  if data['is_paused']: return
  if not jump_web(delayAfter=1.5):
    if data['is_paused']: return
    jump_down_attack(delayAfter=1.5)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x', 0.7) 

  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.5)
  if data['is_paused']: return
  press('left', 1.2)
  if data['is_paused']: return
  release('left', 1)
  press_release('right')
  if data['is_paused']: return
  if not jump_web(delayAfter=1.2):
    if data['is_paused']: return
    jump_down_attack(delayAfter=1.2)
  if data['is_paused']: return
  jump_down_attack(delayAfter=0.7)
  if data['is_paused']: return
  jump_down_attack(delayAfter=0.7)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  jump_down(delayAfter=0.1)
  if data['is_paused']: return
  if not bolt_burst(1.4, rng >= 0.5):
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=1.4)
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x', 0.8) 
  data['just_looted'] = datetime.now() + timedelta(seconds=5)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.6, 2))


def mf3_macro():
  print("Starting Mysterious Fog 3 macro")
  while not data['is_paused']:
    buff()
    mf3_rotation()
    mf3_loot()

def mf3_rotation():
  rng = random.random()
  if datetime.now() > data['next_erda_fountain']:
    press('left')
    jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=1)
    if data['is_paused']: return
    release('left')
    if data['is_paused']: return
    if data['is_paused']: return
    if rng > 0.5 and datetime.now() > data['next_bolt_burst']:
      jump_down(delayAfter=0.15)
      bolt_burst(delayAfter=0.5)
    else:
      jump_down(delayAfter=0.35)
      press_release('q', delay=0.3)
    if data['is_paused']: return
    press('left', delay=1)
    if data['is_paused']: return
    release('left')
    erda_fountain()
    if data['is_paused']: return
    time.sleep(0.5)
    if data['is_paused']: return
    press_release('x')
    press_release('x', 0.8)

  # start from top
  if rng > 0.3:
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.6)
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.45)
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.45)
  else:
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.6)
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    jump_down_attack(delayAfter=0.05)
    if data['is_paused']: return
    press('right', delay=0.45)
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.05)
    if data['is_paused']: return
    release('right', delay=0.45)

  # land on middle
  rng = random.random()
  now = datetime.now()
  if datetime.now() > data['next_web']: 
    jump_down(delayAfter=0.05)
    web(delayAfter=1 if now > data['next_loot_2'] else 0.25)
  else:
    jump_down(delayAfter=0.6 if now > data['next_loot_2'] else 0.2)

  # falling to bottom
  if now > data['next_loot_2']:
    if data['is_paused']: return
    jump_down_attack(attackDelay=0.2, delayAfter=0.6)
    press('left')
    if data['is_paused']: return
    jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.95)
    release('left')
    if data['is_paused']: return
    data['next_loot_2'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.5))
  else:
    if rng > 0.7 and datetime.now() > data['next_bolt_burst']: # 30% chance
      time.sleep(0.4)
      if data['is_paused']: return
      jump_down(delayAfter=0.05)
      if data['is_paused']: return
      bolt_burst(delayAfter=0.6)
    else:
      press_release('left', delay=0.4)
      if data['is_paused']: return
      jump_down_attack(attackDelay=0.2, delayAfter=0.6)
      if data['is_paused']: return
    press('right')
    if data['is_paused']: return
    jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.63)
    if data['is_paused']: return
    if datetime.now() > data['next_loot_3']:
      jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=1)
      data['next_loot_3'] = datetime.now() + timedelta(minutes=0.8)
    release('right')
  if data['is_paused']: return
  press_release('x')
  press_release('x', 0.8)

def mf3_loot():
  if datetime.now() < data['next_loot']:
    return
  rng = random.random()
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.63)
  if data['is_paused']: return
  release('right')
  if data['is_paused']: return
  if data['is_paused']: return
  if rng > 0.5 and datetime.now() > data['next_bolt_burst']:
    jump_down(delayAfter=0.2)
    bolt_burst(delayAfter=1.15)
  else:
    jump_down(delayAfter=0.35)
    press_release('q', delay=1)
  if data['is_paused']: return
  press_release('x')
  if data['is_paused']: return
  press_release('x', 0.8)
  if data['is_paused']: return
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.55))
  rng = random.random()
  press('right')
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.05, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  jump_attack(delayAfter=1)
  if data['is_paused']: return
  release('right')
  if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  if rng > 0.6: 
    jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.68, 0.73))
  if data['is_paused']: return
  release('left', delay=uniform(0.1, 0.3))
  if data['is_paused']: return
  send('x', 0.7)

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
  if cur > data['next_feed_pet']:
    data['next_feed_pet'] = datetime.now() + timedelta(minutes=uniform(2, 3))
    press_release('f10')
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

def jump_web(jumpDelay=0.5, delayAfter=0.3):
  if datetime.now() > data['next_web']:
    jump_down(delayAfter=jumpDelay)
    press_release('4', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=251)
    return True
  return False

def web(delayAfter=0.3):
  if datetime.now() > data['next_web']:
    press_release('4', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=251)
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
  release('up', delay=0.05)
  release('down', delay=0.05)
  release('ctrl', delay=0.05)
  release('alt', delay=0.05)

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


class MoveState:
  STILL = 0
  LEFT = 1
  RIGHT = 2

class Teamviewer:
  def __init__(self):
    self.move_state = MoveState.STILL
    
  def left(self):
    if self.move_state == MoveState.RIGHT: release('right')
    if self.move_state == MoveState.LEFT:
      self.move_state = MoveState.STILL
      release('left')
    else:
      self.move_state = MoveState.LEFT
      press('left')

  def right(self):
    if self.move_state == MoveState.LEFT: release('left')
    if self.move_state == MoveState.RIGHT:
      self.move_state = MoveState.STILL
      release('right')
    else:
      self.move_state = MoveState.RIGHT
      press('right')

  def jump_down(self):
    jump_down()

  def jump_up(self):
    jump_up()

def commands():
  print("Commands:")
  print(f"  {JIAMING_KEY} - write jiaming email")
  print(f"  {JIAMING_PW_KEY} - write jiaming pw")
  print(f"  {JIMMY_KEY} - write jimmy email")
  print(f"  {JIMMY_PW_KEY} - write jimmy pw")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")
  if data['is_teamviewer_enabled']:
    print()
    print("Teamviewer Commands:")
    print(f"  {TEAMVIEW_LEFT} - move left")
    print(f"  {TEAMVIEW_RIGHT} - move right")
    print(f"  {TEAMVIEW_JUMP_DOWN} - jump down")
    print(f"  {TEAMVIEW_JUMP_UP} - jump up")

main()
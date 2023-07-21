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
  'next_sharpeye': datetime.now(),
  'next_split': datetime.now(),
  'current_split_ends_at': datetime.now(),
  'next_surgebolt': datetime.now(),
  'next_loot': datetime.now() + timedelta(minutes=1.2),
  'next_loot_2': datetime.now() + timedelta(minutes=1.2),
  'next_loot_3': datetime.now() + timedelta(minutes=1.2),
  'next_blink_setup': None,
  'next_bully_clear_middle': datetime.now() + timedelta(minutes=0.5),
  'next_web': datetime.now(),
  'next_feed_pet': datetime.now() + timedelta(minutes=1),
  'next_erda_fountain': datetime.now(),
  'next_bird': datetime.now(),
  'next_bolt_burst': datetime.now(),
  'x_and_down_x': False
}

def main():
  commands()
  keyboard.add_hotkey(PAUSE_KEY, pause)
  keyboard.add_hotkey(START_KEY, start)
  while True:
    keyboard.wait(START_KEY)
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.1, 1.45))
    data['next_blink_setup'] = None
    thread = threading.Thread(target=mf3_macro)
    thread.start()
    thread.join()
    release_all()

def mf3_macro():
  print("Starting Mysterious Fog 3 macro")
  while not data['is_paused']:
    buff()
    mf3_rotation()
    mf3_loot()

def mf3_rotation():
  rng = random.random()
  if datetime.now() > data['next_erda_fountain']:
    if data['is_paused']: return
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
    web(delayAfter=0.6 if now > data['next_loot_2'] else 0.2)
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

def plunging_3_macro():
  print("Starting Plunging Depth 3 macro")
  while not data['is_paused']:
    buff()
    plunging_3_loot()
    plunging_3_rotation()

def plunging_3_rotation():
  rng = random.random()
  press_release('left')
  q_and_surgebolt(afterDelay=0.64)
  press_release('right')
  press('down')
  press_release('alt')
  release('down')
  press_release('q', delay=0.6)
  press_release('q', delay=0.7)
  press_release('left')
  if rng > 0.5 and data['next_bolt_burst'] < datetime.now():
    bolt_burst(delayAfter=0.6)
  else:
    q_and_surgebolt(afterDelay=0.64)
  jump_down(delayAfter=0.4)
  if rng > 0.7:
    press_release('right')
    q_and_surgebolt(afterDelay=0.64)
  press('left')
  jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.63)
  jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0)
  release('left', delay=0.63)
  if data['next_erda_fountain'] < datetime.now():
    if data['next_bolt_burst'] < datetime.now():
      press_release('c', delay=1.2)
      bolt_burst(delayAfter=0.8)
    else:
      press_release('c', delay=2)
    press('left', 0.5)
    release('left')
    erda_fountain()
    q_and_surgebolt(afterDelay=0.64)
    press('right')
    jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.63)
    release('right', 0.3)
  elif rng > 0.9:
    jump_attack(jumpDelay=0.2, attackDelay=0.15, delayAfter=0.63)
  press_release('x')
  press_release('x', delay=0.7)

def plunging_3_loot():
  if datetime.now() < data['next_loot']:
    return
  press_release('right')
  flash_jump(jumpDelay=0.4, delayAfter=0.5)
  jump_down(delayAfter=0.7)
  press_release('x')
  press_release('x', delay=0.7)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.2, 1.4))

def mirror_touch_2_macro():
  print("Starting Mirror Touch 2 macro")
  while not data['is_paused']:
    buff()
    mirror_touch_2_rotation()
    # mirror_touch_2_loot()
    mirror_touch_2_loot_vac()

def mirror_touch_2_rotation():
  rng = random.random()
  if datetime.now() < data['current_split_ends_at']:
    q_and_surgebolt(afterDelay=0.63)
  else:
    press_release('alt', delay=0.07)
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.63)
    if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  jump_attack()
  release('left', delay=0.2)
  if data['is_paused']: return
  jump_down_attack(attackDelay=0.4, delayAfter=0.6)
  if data['is_paused']: return
  erda_fountain()
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  jump_attack(jumpDelay=0.2, attackDelay=0.3, delayAfter=0.63)
  if data['is_paused']: return
  jump_attack(jumpDelay=0.2, attackDelay=0.3, delayAfter=0.63)
  if data['is_paused']: return
  if rng > 0.7:
    jump_attack(jumpDelay=0.2, attackDelay=0.3, delayAfter=0.63)
  if data['is_paused']: return
  release('right')
  press_release('x', delay=0.7)

def mirror_touch_2_loot_vac():
  if datetime.now() < data['next_loot']:
    return
  press('left')
  flash_jump(delayAfter=1.5)
  release('left')
  press_release('x', 0.7)
  press('right')
  flash_jump(delayAfter=1.3)
  release('right')
  time.sleep(0.9)
  press_release('x', 0.7)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.2, 1.4))

def mirror_touch_2_loot():
  if datetime.now() < data['next_loot']:
    return
  rng = random.random()
  is_web_left = rng > 0.5

  # vac comment
  press('left', delay=0.5)
  if data['is_paused']: return
  flash_jump(jumpDelay=0.1, delayAfter=0.05)
  if data['is_paused']: return
  press('up', delay=2.2)
  release('up')
  release('left')
  # rng = random.random()
  # if rng > 0.5:
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.8)
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  # else:
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.8)
  #   press_release('left')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7) 
  # time.sleep(0.3)

  if data['is_paused']: return
  jump_down(delayAfter=0.8)
  rng = random.random()
  if is_web_left and data['next_web'] < datetime.now():
    press_release('4', delay=1.3)
    data['next_web'] = datetime.now() + timedelta(minutes=3)
  # vac comment
  # elif rng > 0.5:
  #   press_release('left')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.8)
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  # else:
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  #   press_release('left')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)  
  time.sleep(0.6)

  if data['is_paused']: return
  jump_down(delayAfter=0.8)
  rng = random.random()
  if rng > 0.5:
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.8)
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    press_release('r', delay=0.8)
  else:
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.8)
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=0.7)
  time.sleep(0.6)

  press('right')
  if data['is_paused']: return
  jump_attack(jumpDelay=0.2, attackDelay=0.3, delayAfter=0.63)
  if data['is_paused']: return
  jump_attack(jumpDelay=0.2, attackDelay=0.3, delayAfter=0.63)

  rng = random.random()
  bolt_burst_when_jump = rng > 0.5
  if data['is_paused']: return
  jump_up(delayAfter=0.5 if bolt_burst_when_jump else 1)
  if data['is_paused']: return
  if bolt_burst_when_jump: press_release('d', delay=0.6)
  if data['is_paused']: return
  release('right')
  if not is_web_left and data['next_web'] < datetime.now():
    press_release('4')
    data['next_web'] = datetime.now() + timedelta(minutes=3)
  time.sleep(2.5)
  press('left', delay=0.7)
  release('left')
  if not bolt_burst_when_jump:
    press_release('d')
  time.sleep(0.7)

  if data['is_paused']: return
  # vac comment
  # jump_up(delayAfter=1)
  # rng = random.random()
  # if rng > 0.5:
  #   press_release('left')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  # else:
  #   press_release('right')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  #   press_release('left')
  #   if data['is_paused']: return
  #   q_and_surgebolt(afterDelay=0.7)
  # if data['is_paused']: return
  # time.sleep(0.5)
  # press('right', delay=0.6)
  # release('right')
  # time.sleep(1)

  if data['is_paused']: return
  press_release('x', delay=0.7)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.2, 1.4))

def bully_3_macro():
  print("Starting Bully Blvd 3 macro")
  data['next_bully_clear_middle'] = datetime.now() + timedelta(minutes=0.5)
  while not data['is_paused']:
    rng = random.random()
    buff()
    bully_3_loot(x=False)
    bully_3_rotation()

def bully_3_rotation():
  rng = random.random()
  if data['next_bully_clear_middle'] < datetime.now():
    if data['is_paused']: return
    press('right')
    if data['is_paused']: return
    flash_jump(jumpDelay=0.35, delayAfter=0.05)
    if data['is_paused']: return
    release('right')
    if data['is_paused']: return
    time.sleep(0.7)
    if data['is_paused']: return
    press_release('r', 0.7)
    press_release('x', 0.7)
    data['next_bully_clear_middle'] = datetime.now() + timedelta(minutes=0.5)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  jump_down(delayAfter=1.5)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('up', delay=0.6)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('up', delay=0.6)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('up', delay=0.6)
  if data['is_paused']: return
  press_release('left')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('right')
  if data['is_paused']: return
  q_and_surgebolt(afterDelay=0.63)
  if data['is_paused']: return
  press_release('x', 0.7)
  
def bully_3_loot(x=True):
  if datetime.now() < data['next_loot']:
    return
  if x: press_release('x', 0.7)
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  flash_jump(jumpDelay=0.35, delayAfter=0.05)
  if data['is_paused']: return
  release('right')
  time.sleep(0.5)

  if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  release('left')
  time.sleep(2)
  if data['is_paused']: return
  press('right')
  time.sleep(0.3)
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  release('right')
  
  if data['is_paused']: return
  press('left')
  flash_jump()
  if data['is_paused']: return
  time.sleep(0.8)
  if data['is_paused']: return
  release('left')
  if data['is_paused']: return
  press_release('up')
  press_release('up')

  if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  flash_jump()
  release('left')
  time.sleep(0.5)
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  flash_jump()
  flash_jump()
  time.sleep(0.9)
  if data['is_paused']: return
  release('right')
  if data['is_paused']: return
  jump_down(delayAfter=0.8)
  if data['is_paused']: return
  press('right')
  flash_jump()
  time.sleep(1)
  release('right')
  time.sleep(0.5)

  if data['is_paused']: return
  press('left')
  time.sleep(0.3)
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  flash_jump()
  time.sleep(1)
  release('left')
  time.sleep(2)

  press_release('x', 0.7)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.5))

def laby_cavern_macro():
  print("Starting Laby Cavern macro")
  while not data['is_paused']:
    rng = random.random()
    buff()
    laby_loot()
    laby_cavern_rotation()
    laby_loot()
    laby_cavern_rotation()
    laby_loot()
    laby_cavern_rotation()
    if rng < 0.33:
      laby_cavern_rotation()

def laby_cavern_rotation(): 
  rng = random.random()
  if rng < 0.25:
    # left, right, right, left
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    jump_down(delayAfter=uniform(0.7, 0.9))
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    press_release('q', 0.6)
    if data['is_paused']: return
    press_release('x', 0.7)
  elif rng > 0.25 and rng < 0.5:
    # right, left, left, right
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    jump_down(delayAfter=uniform(0.7, 0.9))
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    press_release('q', 0.6)
    if data['is_paused']: return
    press_release('x', 0.7)
  elif rng > 0.5 and rng < 0.75:
    # left, right, left, right
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    jump_down(delayAfter=uniform(0.7, 0.9))
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    press_release('q', 0.6)
    if data['is_paused']: return
    press_release('x', 0.7)
  else:
    # right, left, right, left
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    jump_down(delayAfter=uniform(0.7, 0.9))
    if data['is_paused']: return
    press_release('right')
    if data['is_paused']: return
    q_and_surgebolt(afterDelay=uniform(0.6, 0.7))
    if data['is_paused']: return
    press_release('left')
    if data['is_paused']: return
    press_release('q', 0.6)
    if data['is_paused']: return
    press_release('x', 0.7)

def laby_loot():
  if datetime.now() < data['next_loot']:
    return
  if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  flash_jump()
  time.sleep(1)
  if data['is_paused']: return
  release('left')
  if data['is_paused']: return
  press('right')
  time.sleep(0.02)
  if data['is_paused']: return
  jump_down()
  if data['is_paused']: return
  flash_jump()
  time.sleep(uniform(0.5, 0.7))
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  release('right')
  time.sleep(uniform(0.9, 1.3))
  press('right')
  if data['is_paused']: return
  flash_jump()
  if data['is_paused']: return
  release('right')
  if data['is_paused']: return
  press('left')
  if data['is_paused']: return
  press_release('c')
  time.sleep(1)
  if data['is_paused']: return
  flash_jump()
  time.sleep(uniform(1.3, 1.6))
  if data['is_paused']: return
  release('left')
  press_release('x', 0.7)
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.1, 1.45))

def water_sun_macro():
  print("Starting 'Where Water and Sunlight Meet' macro")
  while not data['is_paused']:
    rng = random.random()
    buff()
    water_sun_rotation()
    water_sun_rotation()
    water_sun_rotation()
    water_sun_rotation()
    if rng < 0.33:
      water_sun_rotation()
    if rng > 0.33 and rng < 0.66:
      water_sun_rotation()
      water_sun_rotation()

def water_sun_rotation():
  rng = random.random()
  press('left')
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=0.06, delayAfter=0.9)
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.05, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.05, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.05, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.05, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_down_and_fj(delayAfter=0.7)
  if data['is_paused']: return
  release('left')
  if data['is_paused']: return
  press('right')
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
  if data['is_paused']: return
  if rng > 0.6: 
    jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
    if data['is_paused']: return
    if rng > 0.8:
      jump_attack(attackDelay=uniform(0.1, 0.2), jumpDelay=uniform(0.06, 0.09), delayAfter=uniform(0.6, 0.71))
      if data['is_paused']: return
  release('right', delay=uniform(0.1, 0.3))
  if data['is_paused']: return
  send('x', 0.7)

def rev2_macro():
  print("Starting Rev2 macro")
  while not data['is_paused']:
    press('up')
    press_release('alt')
    press_release('alt')
    release('up')
    return
    # rng = random.random()
    # buff()
    # rev2_rotation()
    # rev2_rotation()
    # rev2_rotation()
    # rev2_rotation()
    # if rng < 0.33:
    #   rev2_rotation()
    # if rng > 0.33 and rng < 0.66:
    #   rev2_rotation()
    #   rev2_rotation()

def rev2_rotation():
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
    data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(150, 300))
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

def bolt_burst(delayAfter=0.05):
  press_release('d', delay=delayAfter)
  data['next_bolt_burst'] = datetime.now() + timedelta(seconds=7)

def web(delayAfter=0.3):
  press_release('4', delay=delayAfter)
  data['next_web'] = datetime.now() + timedelta(seconds=251)

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
  time.sleep(delayAfter)
  release('alt')
  release('down')

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
  
def uniform(a, b):
  return random.uniform(a, b)

def commands():
  print("Commands:")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")

main()
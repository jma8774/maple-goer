import time
import random
import threading
import pygame
from datetime import datetime, timedelta
from images import Images

# Create own custom classes to simulate these classes... they use win32/user32 microsoft libraries which flags the events as LowLevelKeyHookInjected
import pyautogui as pag

# Interception library to simulate events without flagging them as LowLevelKeyHookInjected
import interception
from listener import KeyListener
key_pressed = {}

JIAMING_KEY = 'f1'
JIAMING_PW_KEY = 'f2'
JIMMY_KEY = 'f3'
JIMMY_PW_KEY = 'f4'
START_KEY = 'f7'
PAUSE_KEY = 'f8'

ascendion_region = (0, 200, 700, 500)
minimap_rune_region = (0, 0, 200, 200)
rune_region = (370, 200, 80, 80)
thread = None
stop_flag = [False]
audio = { "rune": "images/slaves.mp3", "whiteroom": "images/tyler1autism.mp3" }
data = {
  'is_paused': True,
  'is_changed_map': False,
  'next_loot': datetime.now() + timedelta(minutes=1.5),
  'x_and_down_x': False,

  'next_sharpeye': datetime.now(),
  'next_split': datetime.now(),
  'next_surgebolt': datetime.now(),
  'next_blink_setup': None,
  'next_web': datetime.now(),
  'next_bird': datetime.now(),
  'next_high_speed': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_bolt_burst': datetime.now(),

  'next_rune_check': datetime.now(),
  'next_region_check': datetime.now() - timedelta(seconds=10),
  'minimap_region': None,
}
randomCache = {
  "idx": 0,
  "items": []
}

def main():
  print()

  # Pygame Audio Setup
  setup_audio(volume=1)

  # Interception Setup for main loop
  kdevice = interception.listen_to_keyboard()
  mdevice = interception.listen_to_mouse()
  interception.inputs.keyboard = kdevice
  interception.inputs.mouse = mdevice

  # Interception Key Listener Setup (seperate thread)
  kl = KeyListener(stop_flag)
  kl.add(PAUSE_KEY, pause)
  kl.add(START_KEY, start)
  kl.run()

  tryRegenerateRandomDelays(-0.02, 0.01)
  commands()
  # Bot loop
  try:
    while True:
      if data['is_paused'] == True:
        time.sleep(1)
        continue

      # Setup for each new run
      data['next_blink_setup'] = None
      data['next_region_check'] = datetime.now()
      data['is_changed_map'] = False
      thread = threading.Thread(target=midpoint3_macro)
      thread.start()
      thread.join()
      release_all()

      # Play sound if whiteroomed
      if data['is_changed_map']:
        print(f"Map change detected, playing audio: Press {PAUSE_KEY} to stop")
        play_audio(audio['whiteroom'])
  except KeyboardInterrupt:
    print("Exiting...")
    stop_flag[0] = True
    
def midpoint3_macro():
  def update():
    tryRegenerateRandomDelays(-0.02, 0.01)
    tryRefreshRegions()
    return True

  print("Started World's Sorrow Midpoint 3 macro")
  while update() and not should_pause():
    buff_setup()
    midpoint3_rotation()
    midpoint3_loot()
    release_all()
  print("Paused World's Sorrow Midpoint 3 macro")
    
def midpoint3_rotation():
  mob_loc = None
  rng = random.random()
  if datetime.now() > data['next_erda_fountain']:
    if should_pause(): return
    press_release('shift', 1)
    press('right', 0.3)
    release('right')
    if should_pause(): return
    press_release('left')
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    teleport_reset()
    if should_pause(): return
  
  # Find mob before starting rotation
  count = 0
  while mob_loc == None:
    if should_pause(): return
    mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8, grayscale=True, region=ascendion_region)
    time.sleep(0.4)
    count += 1
    if count > 20: break
  if mob_loc == None:
    print(f"Couldn't find mob after 20 tries, continuing rotation")
  else:
    print(f"Found mob at {mob_loc}, continuing rotation")

  if should_pause(): return
  jump_down_attack(delayAfter=0.4)
  if should_pause(): return
  q_and_surgebolt(afterDelay=0.55)
  if should_pause(): return
  q_and_surgebolt(afterDelay=0.65)
  if should_pause(): return
  press_release('right')
  if not high_speed_shot(0.8, rng > 0.8):
    q_and_surgebolt(afterDelay=0.65)

def midpoint3_loot():
  loot_variation = int(random.random() * 3)
  
  def face_left_teleport_reset():
    if should_pause(): return
    press_release('left', 0.3)
    if should_pause(): return
    teleport_reset()

  if datetime.now() < data['next_loot']:
    face_left_teleport_reset()
    return
  
  rng = random.random()
  rng2 = random.random()
  def right_part():
    if should_pause(): return
    press_release('shift', 1)
    press('right', 0.3)
    release('right')
    if should_pause(): return
    press_release('left')
    if should_pause(): return
    jump_down(delayAfter=0.1)
    if should_pause(): return
    if not bolt_burst(0.6, rng < 0.5):
      q_and_surgebolt(afterDelay=0.6)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    jump_down_attack(delayAfter=1)
    if should_pause(): return
    jump_down_attack(delayAfter=0.7)
    if should_pause(): return
    if not jump_high_speed_shot(delayAfter=0.5, isGo=rng2 > 0.5):
      jump_down_attack(delayAfter=0.5)
    press_release('right', 0.1)
    if should_pause(): return
    if not jump_web(delayAfter=1.5):
      if should_pause(): return
      jump_down_attack(delayAfter=1.5)
    if should_pause(): return
    face_left_teleport_reset()

  def left_part():
    if should_pause(): return
    q_and_surgebolt(afterDelay=0.5)
    if should_pause(): return
    press('left', 1.4)
    if should_pause(): return
    release('left', 0.5)
    press_release('right')
    if should_pause(): return
    if not jump_web(delayAfter=1):
      if should_pause(): return
      jump_down_attack(delayAfter=1)
    if should_pause(): return
    jump_down_attack(delayAfter=0.7)
    if should_pause(): return
    jump_down_attack(delayAfter=0.6)
    if should_pause(): return
    press_release('left')
    press_release('left')
    if should_pause(): return
    jump_down(delayAfter=0.1)
    if should_pause(): return
    if not bolt_burst(1.5, rng >= 0.5):
      if should_pause(): return
      q_and_surgebolt(afterDelay=1.5)
    if should_pause(): return
    teleport_reset()

  if loot_variation == 0:
    if should_pause(): return
    face_left_teleport_reset()
    if should_pause(): return
    right_part()
    if should_pause(): return
    left_part()
  elif loot_variation == 1:
    if should_pause(): return
    face_left_teleport_reset()
    if should_pause(): return
    left_part()
    if should_pause(): return
    right_part()
  else:
    if should_pause(): return
    press('left', 1.4)
    if should_pause(): return
    release('left', 0.7)
    press_release('c', 1.4)
    if should_pause(): return
    if not bolt_burst(0.7):
      if should_pause(): return
      q_and_surgebolt(afterDelay=0.7)
    press_release('right')
    if should_pause(): return
    jump_down_attack(delayAfter=0.55)
    if should_pause(): return
    press_release('left')
    if should_pause(): return
    jump_down_attack(delayAfter=0.7)
    if should_pause(): return
    teleport_reset()
    if should_pause(): return
    right_part()

  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.5, 1.7))

def buff_setup():
  # If rune is up, play some sound
  # if datetime.now() > data['next_rune_check'] and pag.locateOnScreen(Images.RUNE, confidence=0.8, grayscale=True, region=rune_region):
  #   play_audio(audio['rune'])
  #   data['next_rune_check'] = datetime.now() + timedelta(seconds=10)

  if datetime.now() > data['next_rune_check'] and pag.locateOnScreen(Images.RUNE_MINIMAP, confidence=0.8, region=minimap_rune_region):
    play_audio(audio['rune'])
    data['next_rune_check'] = datetime.now() + timedelta(seconds=uniform(50, 60))

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
  if should_pause(): return
  if cur > data['next_sharpeye']:
    data['next_sharpeye'] = datetime.now() + timedelta(seconds=uniform(200, 300))
    press_release('pagedown', 2)
  if should_pause(): return
  if cur > data['next_split']:
    data['next_split'] = datetime.now() + timedelta(seconds=uniform(120, 140))
    press_release('2', 1)
  if should_pause(): return
  if cur > data['next_bird']:
    press_release('5', 0.7)
    data['next_bird'] = datetime.now() + timedelta(seconds=uniform(116, 125))
  if should_pause(): return
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
    return True
  return False

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
  press_release('alt', jumpDelay)
  press_release('alt', delayAfter)

def jump_attack(attackDelay=0.2, jumpDelay=0.05, delayAfter=0.7):
  rng = random.random()
  press_release('alt', jumpDelay)
  press_release('alt', attackDelay)
  press_release('q')
  if rng > 0.7:
    press_release('e')
  time.sleep(delayAfter + getRandomDelay())

def jump_up(delayAfter=1):
  press('up')
  press_release('alt', 0.2)
  press_release('alt')
  press_release('alt')
  release('up', delayAfter)

def jump_down(delayAfter=1):
  press('down', 0.15)
  press('alt', 0.15)
  release('alt')
  release('down', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  press('down')
  press('alt', attackDelay)
  press_release('q')
  release('alt')
  release('down', delayAfter)

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  press('alt')
  release('alt')
  press('alt')
  release('alt', delayAfter)

def q_and_surgebolt(afterDelay=0.7):
  if datetime.now() > data['next_surgebolt']:
    press('q', delay=0.02)
    press_release('e')
    release('q', afterDelay)
    data['next_surgebolt'] = datetime.now() + timedelta(seconds=uniform(10, 13))
  else:
    press_release('q', afterDelay)

def teleport_reset(delayAfter=0.8):
  rng = random.random()
  if should_pause(): return
  press_release('x')
  if should_pause(): return
  press_release('x')
  if rng > 0.33:
    if should_pause(): return
    press_release('x')
  if rng > 0.66:
    if should_pause(): return
    press_release('x')
  if should_pause(): return
  press_release('x', delayAfter)

def tryRefreshRegions():
  if datetime.now() >= data['next_region_check']:
    print("Refreshing regions (180s)")
    minimapLoc = pag.locateOnScreen(Images.MINIMAP, confidence=0.8, grayscale=True)
    data['minimap_region'] = getMinimapRegion(minimapLoc)
    data['next_region_check'] = datetime.now() + timedelta(seconds=180)
  return True

def getMinimapRegion(minimapLoc):
  region = None
  (width, height) = pag.size()
  if not minimapLoc:
    print(" Minimap text not found, returning full screen")
    return (0, 0, width, height)
  x, y = minimapLoc.left, minimapLoc.top
  region = (
      max(0, x-20), max(0, y-20),
      min(55, width-x), min(55, height-y)
    )
  print(" Minimap region: " + str(region))
  return region

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio(audio_file_path):
  pygame.mixer.music.load(audio_file_path)
  pygame.mixer.music.play(loops=-1)

def pause_audio():
  pygame.mixer.music.pause()

def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['is_changed_map'] and pause_if_change_map(Images.LIMINIA_ICON):
    data['is_changed_map'] = True
  return data['is_paused']

def pause_if_change_map(map):
  isSeeMap = pag.locateOnScreen(map, confidence=0.8, region=data['minimap_region'], grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    tryRefreshRegions()
    if pag.locateOnScreen(map, confidence=0.8, region=data['minimap_region'], grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def pause():
  print('Pausing')
  data['is_paused'] = True
  data['x_and_down_x'] = True
  pause_audio()

def start():
  print('\nStarting')
  data['is_paused'] = False

def release_all():
  if isPressed('left'):
    release('left', delay=0.05)
  if isPressed('right'):
    release('right', delay=0.05)
  if isPressed('up'):
    release('up', delay=0.05)
  if isPressed('down'):
    release('down', delay=0.05)
  if isPressed('ctrl'):
    release('ctrl', delay=0.05)
  if isPressed('alt'):
    release('alt', delay=0.05)
  if isPressed('f7'):
    release('f7', delay=0.05)
  if isPressed('f8'):
    release('f8', delay=0.05)
  if isPressed('q'):
    release('q', delay=0.05)
  if isPressed('e'):
    release('e', delay=0.05)
  if isPressed('d'):
    release('d', delay=0.05)

def isPressed(key):
  return key not in key_pressed or key_pressed[key] == False

def press(key, delay=0.05):
  interception.key_down(key)
  key_pressed[key] = True
  time.sleep(delay + getRandomDelay())
  
def release(key, delay=0.05):
  interception.key_up(key)
  key_pressed[key] = False
  time.sleep(delay + getRandomDelay())

def press_release(key, delay=0.05):
  press(key)
  release(key)
  time.sleep(delay + getRandomDelay())
  
def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

def getRandomDelay():
  randomCache['idx'] += 1
  return randomCache['items'][randomCache['idx'] % len(randomCache['items'])]

def tryRegenerateRandomDelays(a, b):
  if randomCache['idx'] < len(randomCache['items']):
    return
  print("Regenerating 10,000,000 random numbers")
  # Generate 10 million random numbers and store it in a list
  randomCache['idx'] = 0
  randomCache['items'] = []
  for _ in range(10000000):
    randomCache['items'].append(uniform(a, b))
  
def commands():
  print(f"Using images for resolution of 1366 fullscreen maplestory")
  print("Commands:")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")
  

if __name__=="__main__":
  main()
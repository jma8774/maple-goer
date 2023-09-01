import time
import random
import threading
import pygame
from datetime import datetime, timedelta
import os 
from base import Images, Audio, KeyListener
import pyautogui as pag
import interception

key_pressed = {}

START_KEY = 'f7'
PAUSE_KEY = 'f8'

monster_region1 = (285, 280, 791-285, 400-280)
monster_region2 = (177, 151, 1355-177, 400-151)
minimap_rune_region = (0, 0, 200, 200)
minimap_map_icon_region = (5, 15, 40, 40)

thread = None
stop_flag = [False]
data = {
  'is_paused': True,
  'is_changed_map': False,

  'next_erda_fountain': datetime.now(),
  'next_burning_sword': datetime.now(),
  'expire_burning_sword': datetime.now(),
  'next_buff': datetime.now(),

  'rune_playing': False,
  'next_rune_check': datetime.now(),
  'next_elite_box_check': datetime.now(),
}
randomCache = {
  "idx": 0,
  "items": []
}

def main():
  clear()

  # Pygame Audio Setup
  setup_audio(volume=1)

  # Interception Setup for main loop
  kdevice = interception.listen_to_keyboard()
  mdevice = interception.listen_to_mouse()
  interception.inputs.keyboard = kdevice
  interception.inputs.mouse = mdevice
  clear()

  # Interception Key Listener Setup (seperate thread)
  kl = KeyListener(stop_flag)
  kl.add(PAUSE_KEY, pause)
  kl.add(START_KEY, start)
  kl.run()
  
  # Bot loop
  try:
    tryRegenerateRandomDelays(-0.02, 0.01)
    commands()
    while True:
      if data['is_paused'] == True:
        time.sleep(1)
        continue

      # Setup for each new run
      setup()
      thread = threading.Thread(target=hidden_macro)
      thread.start()
      thread.join()
      release_all()

      # Play sound if whiteroomed
      if data['is_changed_map']:
        print(f"Map change detected, script paused, playing audio: Press {PAUSE_KEY} to stop")
        play_audio(Audio.TYLER1_AUTISM)
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    stop_flag[0] = True
    
def setup():
  data['is_changed_map'] = False
  
def hidden_macro():
  print("Started Hidden Research Train macro")
  while not should_pause():
    tryRegenerateRandomDelays(-0.02, 0.01)
    buff_setup()
    hidden_rotation()
    release_all()
  print("Paused Hidden Research Train macro")
    
def hidden_rotation():
  def wait_for_spawn(region):
    # Find mob before starting rotation
    mob_loc = None
    count = 0
    while mob_loc == None:
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.DRONE_A, confidence=0.75, grayscale=True, region=region) or pag.locateOnScreen(Images.DRONE_B, confidence=0.75, grayscale=True, region=region)
      time.sleep(0.2)
      count += 1
      if count > 30: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")

  rng = random.random()
  wait_for_spawn(region=monster_region1)
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  press_release('right')

  place_stationary = datetime.now() > data['expire_burning_sword'] and (datetime.now() > data['next_erda_fountain'] or datetime.now() > data['next_burning_sword'])
  if place_stationary:
    jump_attack()
    if should_pause(): return
    press_release('x', 1.1)
    if should_pause(): return
    if not burning_sword():
      erda_fountain()
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
  else:
    if should_pause(): return
    wait_for_spawn(region=monster_region2)
    if should_pause(): return
    jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if rng > 0.7:
    jump_attack()
  press_release('left')

def buff_setup():
  cur = datetime.now()
  
  if cur > data['next_elite_box_check']:
    boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
    print(boxloc)
    played = False
    while boxloc != None:
      if not played: 
        play_audio(Audio.PING, loops=1)
        played = True
      interception.click(x=boxloc.x, y=boxloc.y, clicks=3)
      time.sleep(0.5)
      boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
    data['next_elite_box_check'] = cur + timedelta(seconds=45)

  if cur > data['next_rune_check']:
    if pag.locateOnScreen(Images.RUNE_MINIMAP, confidence=0.7, region=minimap_rune_region):
      if not data['rune_playing']:
        play_audio(Audio.get_random_rune_audio())
        data['rune_playing'] = True
    if pag.locateOnScreen(Images.BOUNTY_MINIMAP, region=minimap_rune_region):
      play_audio(Audio.PING, loops=1)
    data['next_rune_check'] = cur + timedelta(seconds=45)

  if cur > data['next_buff']:
    press_release('pagedown', 2)
    data['next_buff'] = cur + timedelta(seconds=190)
    
def subway3_macro():
  print("Started Subway Tunnel 3 macro")
  while not should_pause():
    tryRegenerateRandomDelays(-0.02, 0.01)
    buff_setup()
    subway3_rotation()
    release_all()
  print("Paused Subway Tunnel 3 macro")
    
def subway3_rotation():
  def wait_for_spawn(region):
    # Find mob before starting rotation
    mob_loc = None
    count = 0
    while mob_loc == None:
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.MONTO, confidence=0.75, grayscale=True, region=region) or pag.locateOnScreen(Images.MONTO2, confidence=0.75, grayscale=True, region=region)
      time.sleep(0.2)
      count += 1
      if count > 30: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")

  use_fountain = datetime.now() > data['next_erda_fountain']
  rng = random.random()
  if use_fountain:
    jump_attack()
    if should_pause(): return
    press_release('x', 1.1)
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
    if should_pause(): return
    jump_down_attack(delayAfter=0.5)
  if not use_fountain:
    wait_for_spawn(region=monster_region1)
    if should_pause(): return
    jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  press_release('right')
  if should_pause(): return
  wait_for_spawn(region=monster_region2)
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if should_pause(): return
  jump_attack()
  if rng > 0.7:
    jump_attack()
  press_release('left')

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    press('down')
    press_release('f4')
    press_release('f4')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def burning_sword():
  if datetime.now() > data['next_burning_sword']:
    press_release('3', 0.8)
    press_release('3', 0.8)
    data['expire_burning_sword'] = datetime.now() + timedelta(seconds=63)
    data['next_burning_sword'] = datetime.now() + timedelta(seconds=120)
    return True
  return False

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  press_release('e', jumpDelay)
  press_release('e', delayAfter)

def jump_attack(attackDelay=0.15, jumpDelay=0.04, delayAfter=0.5):
  rng = random.random()
  press_release('e', jumpDelay)
  press_release('e', attackDelay)
  press_release('w')
  time.sleep(delayAfter + getRandomDelay())

def jump_up(delayAfter=1):
  press('up')
  press_release('e', 0.2)
  press_release('e')
  press_release('e')
  release('up', delayAfter)

def jump_down(delayAfter=1):
  press('down', 0.15)
  press('e', 0.15)
  release('e')
  release('down', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  press('down')
  press('e', attackDelay)
  press_release('w')
  release('e')
  release('down', delayAfter)

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  press('e')
  release('e')
  press('e')
  release('e', delayAfter)

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio(audio_file_path, loops=-1):
  pygame.mixer.music.load(audio_file_path)
  pygame.mixer.music.play(loops=loops)

def pause_audio():
  pygame.mixer.music.pause()

def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['is_changed_map'] and pause_if_change_map(Images.REVERSE_ICON):
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

def pause():
  print('Pausing')
  data['is_paused'] = True
  data['rune_playing'] = False
  data['x_and_down_x'] = True
  pause_audio()

def start():
  print('\nStarting')
  data['is_paused'] = False

def reset_loot_timer():
  print('\nResetting loot timer')
  data['next_loot'] = datetime.now() + timedelta(minutes=1.7)

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
  if isPressed('e'):
    release('e', delay=0.05)
  if isPressed('f7'):
    release('f7', delay=0.05)
  if isPressed('f8'):
    release('f8', delay=0.05)
  if isPressed('w'):
    release('w', delay=0.05)
  if isPressed('r'):
    release('r', delay=0.05)
  if isPressed('d'):
    release('d', delay=0.05)

def isPressed(key):
  return key in key_pressed and key_pressed[key] == True

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
  release(key, delay)
  
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

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

if __name__=="__main__":
  main()
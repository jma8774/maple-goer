import time
import random
import threading
import pygame
import pyautogui as pag
from datetime import datetime, timedelta
import os
from base import Images, Audio, KeyListener
import interception
key_pressed = {}

START_KEY = 'f7'
PAUSE_KEY = 'f8'

monster_region = (800, 0, 600, 300)
minimap_map_icon_region = (5, 15, 40, 40)

thread = None
stop_flag = [False]
data = {
  'is_paused': True,
  'is_changed_map': False,

  'next_loot': datetime.now() + timedelta(minutes=1.3),
  # 'next_loot': datetime.now() + timedelta(minutes=0),
  'next_gale_barrier': datetime.now(),
  'next_monsoon': datetime.now(),
  'next_sphere': datetime.now(),
  'next_merciless_wind': datetime.now(),
  'next_howling': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_phalanx_charge': datetime.now(),
  'next_web': datetime.now(),
  'next_cast': datetime.now(),

  'next_rune_check': datetime.now(),
}

def main():
  clear()
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

  try:
    commands()
    while True:
      if data['is_paused'] == True:
        time.sleep(2)
        continue
      # Setup for each new run
      data['is_changed_map'] = False
      thread = threading.Thread(target=end_1_5_macro)
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

def end_1_5_macro():
  print("Started End of World 1-5 macro")
  while not should_pause():
    # If rune is up, play some sound
    # if datetime.now() > data['next_rune_check'] and pag.locateOnScreen(images['rune'], confidence=0.8, grayscale=True):
    #   play_audio(Audio.get_random_rune_audio())
    #   data['next_rune_check'] = datetime.now() + timedelta(seconds=20)
    end_1_5_rotation()
    release_all()
  print("Paused End of World 1-5 macro")

def end_1_5_rotation():
  rng = random.random()
  gale_barrier()
  if should_pause(): return
  if not sphere():
    if should_pause(): return
    if not monsoon():
      if should_pause(): return
      howling_gale()
  if should_pause(): return
  if should_pause(): return
  if not merciless_winds():
    phalanx_charge()
  if should_pause(): return
  web()
  if rng > 0.5:
    press_release('d', 0.6)
  if should_pause(): return
  if datetime.now() > data['next_loot']:
    end_1_5_looting()
  else:
    press('a', 3)
    if should_pause(): return
    # Find mob before continuing
    count = 0
    mob_loc = None
    while mob_loc == None:
      if should_pause(): return
      mob_loc = pag.locateOnScreen(Images.ASCENDION, confidence=0.8, grayscale=True, region=monster_region)
      time.sleep(0.3)
      count += 1
      if count > 20: break
    if mob_loc == None:
      print(f"Couldn't find mob after {count} tries, continuing rotation")
    else:
      print(f"Found mob at {mob_loc}, continuing rotation")
    if should_pause(): return
    release('a')
    if should_pause(): return

def end_1_5_looting():
  if datetime.now() > data['next_loot']:
    if should_pause(): return
    press('left')
    if should_pause(): return
    jump_attack(delayAfter=0.7)
    if should_pause(): return
    jump_attack(delayAfter=0.74)
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    release('left')
    if should_pause(): return
    erda_fountain()
    if should_pause(): return
    time.sleep(1.5)
    if should_pause(): return
    press('right')
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack(jumpDelay=0.3)
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    release('right')
    if should_pause(): return
    jump_up(jumpDelay=0.3, delayAfter=0.6)
    if should_pause(): return
    press_release('left')
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.4, 1.6))
    # data['next_loot'] = datetime.now() + timedelta(minutes=0.2)

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio(audio_file_path):
  pygame.mixer.music.load(audio_file_path)
  pygame.mixer.music.play(loops=-1)

def pause_audio():
  pygame.mixer.music.pause()

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    press('down')
    press_release('f4')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def gale_barrier(delayAfter=0.8):
  if datetime.now() > data['next_gale_barrier']:
    press_release('e', delay=delayAfter)
    data['next_gale_barrier'] = datetime.now() + timedelta(seconds=90)
    return True
  return False  

def monsoon(delayAfter=1.1):
  if datetime.now() > data['next_monsoon']:
    press_release('r', delay=delayAfter)
    data['next_monsoon'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False  

def sphere(delayAfter=0.9):
  if datetime.now() > data['next_sphere']:
    press_release('y', delay=delayAfter)
    data['next_sphere'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False

def merciless_winds(delayAfter=0.7):
  if datetime.now() > data['next_merciless_wind']:
    press_release('f', delay=delayAfter)
    data['next_merciless_wind'] = datetime.now() + timedelta(seconds=10)
    return True
  return False

def howling_gale(delayAfter=0.9):
  if datetime.now() > data['next_howling']:
    press_release('t', delay=delayAfter)
    data['next_howling'] = datetime.now() + timedelta(seconds=5)
    return True
  return False

def phalanx_charge(delayAfter=0.8):
  if datetime.now() > data['next_phalanx_charge']:
    press_release('g', delay=delayAfter)
    data['next_phalanx_charge'] = datetime.now() + timedelta(seconds=30)
    return True
  return False

def web(delayAfter=0.6):
  if datetime.now() > data['next_web']:
    press_release('shift', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False
  
def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['is_changed_map'] and pause_if_change_map(Images.LIMINIA_ICON):
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

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  press_release('space', jumpDelay)
  press_release('space', delayAfter)

def jump_attack(attackDelay=0.05, jumpDelay=0.03, delayAfter=0.55):
  press_release('space', jumpDelay)
  press_release('space', attackDelay)
  press_release('d', delayAfter)

def jump_up(jumpDelay=0.2, delayAfter=1):
  press('up')
  press_release('space', jumpDelay)
  press_release('space')
  release('up', delayAfter)
  
def jump_down(delayAfter=1):
  press('down', 0.15)
  press('space', 0.15)
  release('space')
  release('down', delayAfter)

def jump_down_attack(attackDelay=0.05, delayAfter=1):
  press('down')
  press('space', attackDelay)
  press_release('d', delayAfter)
  release('space')
  release('down')

def jump_down_and_fj(delayAfter=1):
  jump_down(delayAfter=uniform(0.3, 0.5))
  press_release('space')
  press_release('space', delayAfter)

def pause():
  print('Pausing')
  data['is_paused'] = True
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
  if isPressed('space'):
    release('space', delay=0.05)
  release('a', delay=0.05)
  if isPressed('a'):
    release('a', delay=0.05)

def isPressed(key):
  return key in key_pressed and key_pressed[key] == True

def press(key, delay=0.05):
  interception.key_down(key)
  key_pressed[key] = True
  time.sleep(delay)
  
def release(key, delay=0.05):
  interception.key_up(key)
  key_pressed[key] = False
  time.sleep(delay)

def press_release(key, delay=0.05):
  press(key)
  release(key)
  time.sleep(delay)
  
def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

def commands():
  print("Commands:")
  print(f"  {START_KEY} - start")
  print(f"  {PAUSE_KEY} - pause")

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

main()
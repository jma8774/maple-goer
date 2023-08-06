import time
import keyboard
import random
import threading
import pygame
import pyautogui as pag
from datetime import datetime, timedelta

START_KEY = 'f7'
PAUSE_KEY = 'f8'

images = {
  "rune": "rune1366.png",
  "liminia": "liminia_icon.png",
  "minimap": "minimap.png",
  "ascendion": "ascendion.png"
}
audio = { "rune": "slaves.mp3", "whiteroom": "tyler1autism.mp3" }
monster_region = (800, 0, 600, 300)

logging = False
thread = None
data = {
  'is_paused': True,
  'is_changed_map': False,

  'next_loot': datetime.now() + timedelta(minutes=1.3),
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
  'next_region_check': datetime.now() - timedelta(seconds=10),
  'minimap_region': None,
}

def main():
  commands()
  setup_audio(volume=1)
  keyboard.add_hotkey(PAUSE_KEY, pause)
  keyboard.add_hotkey(START_KEY, start)
  while True:
    keyboard.read_key()
    if data['is_paused'] == True:
      continue
    # Setup for each new run
    data['next_region_check'] = datetime.now()
    data['is_changed_map'] = False
    thread = threading.Thread(target=end_1_5_macro)
    thread.start()
    thread.join()
    release_all()

    # Play sound if whiteroomed
    if data['is_changed_map']:
      print(f"Map change detected, playing audio: Press {PAUSE_KEY} to stop")
      play_audio(audio['whiteroom'])

def end_1_5_macro():
  print("Started End of World 1-5 macro")
  while refreshRegions() and not should_pause():
    # If rune is up, play some sound
    # if datetime.now() > data['next_rune_check'] and pag.locateOnScreen(images['rune'], confidence=0.8, grayscale=True):
    #   play_audio(audio['rune'])
    #   data['next_rune_check'] = datetime.now() + timedelta(seconds=20)
    end_1_5_rotation()
    end_1_5_looting()
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
    press_release('d', 0.8)
  if should_pause(): return
  press('a', 3)
  if should_pause(): return
  mob_loc = None
  while not mob_loc:
    if should_pause(): return
    time.sleep(0.2)
    mob_loc = pag.locateOnScreen(images['ascendion'], confidence=0.9, grayscale=True, region=monster_region)
  print(f"Found a mob at location {mob_loc}")
  if should_pause(): return
  release('a')
  if should_pause(): return

def end_1_5_looting():
  if datetime.now() > data['next_loot']:
    if should_pause(): return
    press('left')
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack()
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
    jump_attack()
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    jump_attack()
    if should_pause(): return
    release('right')
    if should_pause(): return
    jump_up(jumpDelay=0.4, delayAfter=0.6)
    if should_pause(): return
    press_release('left')
    if should_pause(): return
    press_release('left')
    data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.2, 1.6))

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
    press_release('f4')
    release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def gale_barrier(delayAfter=0.8):
  if datetime.now() > data['next_gale_barrier']:
    press_release('e')
    press_release('e', delay=delayAfter)
    data['next_gale_barrier'] = datetime.now() + timedelta(seconds=90)
    return True
  return False  

def monsoon(delayAfter=1.1):
  if datetime.now() > data['next_monsoon']:
    press_release('r')
    press_release('r', delay=delayAfter)
    data['next_monsoon'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False  

def sphere(delayAfter=0.9):
  if datetime.now() > data['next_sphere']:
    press_release('y')
    press_release('y', delay=delayAfter)
    data['next_sphere'] = datetime.now() + timedelta(seconds=29.7)
    return True
  return False

def merciless_winds(delayAfter=0.7):
  if datetime.now() > data['next_merciless_wind']:
    press_release('f')
    press_release('f', delay=delayAfter)
    data['next_merciless_wind'] = datetime.now() + timedelta(seconds=10)
    return True
  return False

def howling_gale(delayAfter=0.9):
  if datetime.now() > data['next_howling']:
    press_release('t')
    press_release('t', delay=delayAfter)
    data['next_howling'] = datetime.now() + timedelta(seconds=5)
    return True
  return False

def phalanx_charge(delayAfter=0.8):
  if datetime.now() > data['next_phalanx_charge']:
    press_release('g')
    press_release('g', delay=delayAfter)
    data['next_phalanx_charge'] = datetime.now() + timedelta(seconds=30)
    return True
  return False

def web(delayAfter=0.6):
  if datetime.now() > data['next_web']:
    press_release('shift')
    press_release('shift', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=250)
    return True
  return False
  
def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if not data['is_changed_map'] and pause_if_change_map(images['liminia']):
    data['is_changed_map'] = True
  return data['is_paused']

def pause_if_change_map(map):
  isSeeMap = pag.locateOnScreen(map, confidence=0.8, region=data['minimap_region'], grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    refreshRegions()
    if pag.locateOnScreen(map, confidence=0.8, region=data['minimap_region'], grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def refreshRegions():
  if datetime.now() >= data['next_region_check']:
    print("Refreshing regions (180s)")
    minimapLoc = pag.locateOnScreen(images['minimap'], confidence=0.8, grayscale=True)
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
      min(100, width-x), min(100, height-y)
    )
  print(" Minimap region: " + str(region))
  return region

def flash_jump(jumpDelay=0.2, delayAfter=0.7):
  press_release('space')
  time.sleep(jumpDelay)
  press_release('space')
  time.sleep(delayAfter)

def jump_attack(attackDelay=0.1, jumpDelay=0.05, delayAfter=0.7):
  press_release('space', jumpDelay)
  press_release('space')
  press_release('space', attackDelay)
  keyboard.send('d')
  time.sleep(delayAfter)

def jump_up(jumpDelay=0.2, delayAfter=1):
  press('up')
  press_release('space', jumpDelay)
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
  print('Pausing')
  data['is_paused'] = True
  pause_audio()

def start():
  print('\nStarting')
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
  if keyboard.is_pressed('space'):
    release('space', delay=0.05)
  release('a', delay=0.05)
  if keyboard.is_pressed('a'):
    release('a', delay=0.05)

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
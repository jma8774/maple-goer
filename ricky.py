import time
import random
import threading
from datetime import datetime, timedelta
import pyautogui as pag
import pygame
from images import Images

# Interception library to simulate events without flagging them as LowLevelKeyHookInjected
import interception
from listener import KeyListener
key_pressed = {}

START_KEY = 'f7'
PAUSE_KEY = 'f8'

audio = { "rune": "images/slaves.mp3", "whiteroom": "images/tyler1autism.mp3" }
monster_region = (800, 15, 560, 290)
minimap_map_icon_region = (5, 15, 40, 40)

thread = None
stop_flag = [False]
data = {
  'is_paused': True,
  'is_changed_map': False,
  'next_loot': datetime.now() + timedelta(minutes=0.1),

  'next_fire_floor': datetime.now(),
  'next_erda_fountain': datetime.now(),
  'next_fire_breath': datetime.now(),
  'next_wind_breath': datetime.now(),
  'next_dark_fog': datetime.now(),
  'next_onyx_dragon': datetime.now(),
  'next_web': datetime.now(),
}

def main():
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

  commands()
  try:
    while True:
      if data['is_paused'] == True:
        time.sleep(2)
        continue
      data['is_changed_map'] = False
      thread = threading.Thread(target=liminia_1_5_macro)
      thread.start()
      thread.join()
      release_all()

      # Play sound if whiteroomed
      if data['is_changed_map']:
        print(f"Map change detected, script paused, playing audio: Press {PAUSE_KEY} to stop")
        play_audio(audio['whiteroom'])
  except KeyboardInterrupt:
    print("Exiting...")
    stop_flag[0] = True

def liminia_1_5_macro():
  print("Starting 1-5 macro")
  while not should_pause():
    liminia_1_5_rotation()
    release_all()

def liminia_1_5_rotation():
  # Find mob before starting rotation
  start_wait = datetime.now()
  mob_loc = pag.locateOnScreen(Images.FOREBERION, region=monster_region, confidence=0.8)
  while mob_loc == None:
    if should_pause(): return
    mob_loc = pag.locateOnScreen(Images.FOREBERION, region=monster_region, confidence=0.8)
    time.sleep(0.3)
    if datetime.now() - start_wait > timedelta(seconds=7):
      break
  if mob_loc == None:
    print(f"Couldn't find mob after 7 secs, continuing rotation")
  else:
    print(f"Found mob at {mob_loc}, continuing rotation")

  if fire_breath():
    if datetime.now() > data['next_fire_floor']:
      press('left')
      if should_pause(): return
      teleport()
      if should_pause(): return
      teleport()
      if should_pause(): return
      teleport()
      if should_pause(): return
      press_release('ctrl')
      if should_pause(): return
      release('left')
      if should_pause(): return
      if datetime.now() > data['next_erda_fountain']:
        press('left')
        teleport()
        if should_pause(): return
        release('left')
        if should_pause(): return
        erda_fountain()
        press('right')
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        release('right')
        press_release('left')
        if should_pause(): return
      else:
        press('right')
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        teleport()
        if should_pause(): return
        release('right')
        if should_pause(): return
        press_release('left')
        if should_pause(): return
      data['next_fire_floor'] = datetime.now() + timedelta(seconds=uniform(15, 20))
    else:
      dark_fog()
      liminia_1_5_loot()
  else:
    wind_breath()
    dark_fog()
    liminia_1_5_loot()
  time.sleep(1)


def liminia_1_5_loot():
  if datetime.now() < data['next_loot']:
    return
  if should_pause(): return
  press('up')
  if should_pause(): return
  teleport()
  if should_pause(): return
  release('up')
  if should_pause(): return
  press('left', 2)
  if should_pause(): return
  release('left')

  # Use spider web or onyx on top
  if not summon_web():
    if datetime.now() > data['next_onyx_dragon']:
      if should_pause(): return
      press('up')
      if should_pause(): return
      teleport()
      if should_pause(): return
      release('up')
      if should_pause(): return
      summon_onyx()
      if should_pause(): return
      press('down')
      if should_pause(): return
      teleport()
      if should_pause(): return
      release('down')

  if should_pause(): return
  press('down')
  if should_pause(): return
  teleport()
  release('down')
  if should_pause(): return
  press('right')
  if should_pause(): return
  teleport()
  if should_pause(): return
  teleport()
  # # if should_pause(): return
  # # teleport()
  if should_pause(): return
  release('right')
  if should_pause(): return
  press_release('left')
  data['next_loot'] = datetime.now() + timedelta(minutes=uniform(1.3, 1.7))
  return True

def dark_fog():
  if datetime.now() < data['next_dark_fog']:
    return
  press_release('pagedown', 0.7)
  data['next_dark_fog'] = datetime.now() + timedelta(seconds=uniform(40, 50))
  
def fire_breath():
  if datetime.now() > data['next_fire_breath']:
    press_release('g')
    press_release('t', 0.7)
    data['next_fire_breath'] = datetime.now() + timedelta(seconds=10)
    return True
  return False
  
def wind_breath():
  if datetime.now() > data['next_wind_breath']:
    press_release('a')
    press_release('f', 0.7)
    data['next_wind_breath'] = datetime.now() + timedelta(seconds=8)
    return True
  return False

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

def teleport(delay=0.6):
  press_release('d', delay)

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
  release('up', delayAfter)

def jump_down(delayAfter=1):
  press('down', 0.15)
  press('w', 0.15)
  release('w')
  release('down', delayAfter)

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
  isSeeMap = pag.locateOnScreen(map, confidence=0.8, region=minimap_map_icon_region, grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    if pag.locateOnScreen(map, confidence=0.8, region=minimap_map_icon_region, grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def pause():
  print('Pause')
  data['is_paused'] = True
  pause_audio()

def start():
  print('Start')
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

def isPressed(key):
  return key not in key_pressed or key_pressed[key] == False

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

main()
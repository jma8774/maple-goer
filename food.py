import time
import threading
import pygame
from datetime import datetime, timedelta
from images import Images
import pyautogui as pag

# Interception library to simulate events without flagging them as LowLevelKeyHookInjected
import interception
from listener import KeyListener
key_pressed = {}

REFRESH_MOUSE_POSITION_KEY = 'f1'
LUCID_KEY = 'f2'
WILL_KEY = 'f3'

thread = None
stop_flag = [False]
data = {
  'corner_pos': (0, 0),
  'script': None,
}

def main():
  print()

  # Pygame Audio Setup
  setup_audio(volume=0.5)

  # Interception Setup for main loop
  kdevice = interception.listen_to_keyboard()
  mdevice = interception.listen_to_mouse()
  interception.inputs.keyboard = kdevice
  interception.inputs.mouse = mdevice

  # Interception Key Listener Setup (seperate thread)
  kl = KeyListener(stop_flag)
  kl.add(REFRESH_MOUSE_POSITION_KEY, refresh_mouse_position)
  kl.add(LUCID_KEY, lambda: script(lucid.__name__, lucid))
  kl.add(WILL_KEY, lambda: script(will.__name__, will))
  kl.run()

  # Bot loop
  try:
    commands()
    while True:
      if data['script'] == None:
        time.sleep(1)
        continue
      thread = threading.Thread(target=data['script'][1])
      thread.start()
      thread.join()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    stop_flag[0] = True

def lucid():
  while data['script'] and data['script'][0] == lucid.__name__:
    if pag.locateOnScreen(Images.LUCID, confidence=0.8, region=(data['corner_pos'][0]+700, data['corner_pos'][1]+150, 200, 125), grayscale=True):
      print(lucid.__name__)
      play_audio()
      time.sleep(3)
    time.sleep(0.2)

def will():
  while data['script'] and data['script'][0] == will.__name__:
    if pag.locateOnScreen(Images.WILL, confidence=0.8, region=(data['corner_pos'][0]+1065, data['corner_pos'][1]+175, 300, 100), grayscale=True):
      print(will.__name__)
      play_audio()
      time.sleep(3)
    time.sleep(0.2)

def script(key, fn):
  if data['script'] and data['script'][0] == key:
    data['script'] = None
  else:
    print()
    print("Starting script:", key)
    data['script'] = (key, fn)

def refresh_mouse_position():
  data['corner_pos'] = pag.position()
  print(f"Refreshing mouse position for maplestory top left corner to {data['corner_pos']}")

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio():
  pygame.mixer.music.load("images/ping.mp3")
  pygame.mixer.music.play()

def pause_audio():
  pygame.mixer.music.pause()

def commands():
  print("Commands:")
  print(f"  {REFRESH_MOUSE_POSITION_KEY} - refresh mouse position at top left corner of maplestory window")
  print(f"  {LUCID_KEY} - start/stop lucid boss detection")
  print(f"  {WILL_KEY} - start/stop will boss detection")
  

if __name__=="__main__":
  main()
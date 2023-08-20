import time
import threading
import pygame
from datetime import datetime, timedelta
from images import Images
import pyautogui as pag
import os

# Interception library to simulate events without flagging them as LowLevelKeyHookInjected
import interception
from listener import KeyListener

START_STOP_KEY = 'f1'

thread = None
stop_flag = [False]
data = {
  'script': None,
}

def main():
  clear()

  # Pygame Audio Setup
  setup_audio(volume=0.5)

  # Interception Setup for main loop
  kdevice = interception.listen_to_keyboard()
  mdevice = interception.listen_to_mouse()
  interception.inputs.keyboard = kdevice
  interception.inputs.mouse = mdevice
  clear()

  # Interception Key Listener Setup (seperate thread)
  kl = KeyListener(stop_flag)
  kl.add(START_STOP_KEY, lambda: script(fuse_familiars.__name__, fuse_familiars))
  kl.run()

  # Bot loop
  try:
    commands()
    while True:
      if data['script'] == None:
        time.sleep(1)
        continue
      thread = threading.Thread(target=reset_on_exception(data['script'][1]))
      thread.start()
      thread.join()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    stop_flag[0] = True

def fuse_familiars():
  # Required locations
  fam_fusion_loc = pag.locateOnScreen(Images.FAM_FUSION, confidence=0.9, grayscale=True)
  if not fam_fusion_loc:
    raise Exception("Could not find familiar UI at the Collection -> Fusion tab")
  fam_equip_tab = pag.locateOnScreen(Images.FAM_EQUIP, confidence=0.9, grayscale=True)
  if not fam_equip_tab:
    raise Exception("Could not find inventory at the USE tab")

  # Regions
  fam_ui_region = (fam_fusion_loc.left, fam_fusion_loc.top, 750, 435)
  fam_inventory_region = (fam_equip_tab.left, fam_equip_tab.top, 675, 390)

  # Cached locations
  fam_locs = list(map(lambda x: pag.center(x), pag.locateAllOnScreen(Images.FAM_ASCENDION, confidence=0.9, grayscale=True, region=fam_ui_region)))
  fam_hover = (fam_fusion_loc.left+85, fam_fusion_loc.top+180)
  fam_cancel = None
  fam_select_all = None
  fam_fuse = None
  fam_rankup = None

  fusing = False

  def can_continue():
    return data['script'] and data['script'][0] == fuse_familiars.__name__
  
  def check_if_valid():
    nonlocal i, fusing
    interception.click(fam_locs[i].x, fam_locs[i].y, delay=0.5)
    interception.move_to(fam_hover)
    time.sleep(0.25)
    if pag.locateOnScreen(Images.FAM_STOP, confidence=0.9, grayscale=True, region=fam_ui_region):
      print("Found familiar to stop at")
      i = 100000
      return False
    if not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True, region=fam_ui_region):
      interception.move_to(fam_ui_region)
      return False
    interception.move_to(fam_ui_region)
    fusing = True
    print("Found valid")
    return True
  
  def cancel():
    nonlocal fam_cancel
    interception.move_to(fam_ui_region)
    time.sleep(0.2)
    if not fam_cancel:
      fam_cancel = pag.locateCenterOnScreen(Images.FAM_CANCEL, confidence=0.8, grayscale=True, region=fam_ui_region)
    if not fam_cancel:
      raise Exception("Could not find familiar cancel button")
    interception.click(fam_cancel)
    interception.click(fam_cancel, delay=0.25)

  def select_all_fuse():
    nonlocal fam_select_all, fam_fuse
    while can_continue() and pag.locateOnScreen(Images.FAM_ASCENDION, confidence=0.9, grayscale=True, region=fam_ui_region):
      if not fam_select_all:
        fam_select_all = pag.locateCenterOnScreen(Images.FAM_SELECT_ALL, confidence=0.9, grayscale=True, region=fam_ui_region)
      if not fam_select_all:
        raise Exception("Could not find select all button")
      interception.click(fam_select_all, delay=0.25)
      if not fam_fuse:
        fam_fuse = pag.locateCenterOnScreen(Images.FAM_FUSE_ACTIVE, confidence=0.9, grayscale=True, region=fam_ui_region)
      if not fam_fuse:
        raise Exception("Could not find fuse button")
      interception.click(fam_fuse)
      interception.click(fam_fuse, delay=0.25)
      press_release("enter")
      press_release("enter")
      press_release("enter")
      time.sleep(0.25)

  def open_25_familiars():
    stack = pag.locateCenterOnScreen(Images.FAM_100_STACK, region=fam_inventory_region) or \
            pag.locateCenterOnScreen(Images.FAM_75_STACK, region=fam_inventory_region) or \
            pag.locateCenterOnScreen(Images.FAM_50_STACK, region=fam_inventory_region) or \
            pag.locateCenterOnScreen(Images.FAM_25_STACK, region=fam_inventory_region)
    if not stack:
      raise Exception("Could not find 100, 75, 50, 25 familiar stacks to open in inventory")
    interception.click(stack)
    interception.click(stack)
    interception.click(stack)
    press_release("2")
    press_release("5")
    press_release("enter")
    press_release("enter")
    press_release("enter")
    time.sleep(0.25)
  
  def rank_up():
    nonlocal fam_rankup
    can_rank_up = pag.locateOnScreen(Images.FAM_RARE_FULL_POINTS, confidence=0.95, grayscale=True, region=fam_ui_region) or \
                  pag.locateOnScreen(Images.FAM_EPIC_FULL_POINTS, confidence=0.95, grayscale=True, region=fam_ui_region)
    if can_rank_up:
      time.sleep(3)
      if not fam_rankup:
        fam_rankup = pag.locateCenterOnScreen(Images.FAM_RANK_UP, confidence=0.9, grayscale=True, region=fam_ui_region)
      if not fam_rankup:
        raise Exception("Could not find select all button")
      interception.click(fam_rankup)
      interception.click(fam_rankup, delay=0.25)
      press_release("enter")
      press_release("enter")
      press_release("enter")
      time.sleep(6)
      print("Rank up")
      # Check if familiar is level 1 so we know is rank up was successful
      interception.move_to(fam_hover)
      time.sleep(0.25)
      ranked_up = not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True, region=fam_ui_region)
      print("Ranked up" if ranked_up else "Failed to rank up")
      return ranked_up
    return False
  
  i = 0
  while can_continue():
    if i >= len(fam_locs):
      print("Finished fusing familiars")
      data['script'] = None
      break
    
    if not fusing and not check_if_valid():
      i += 1
      cancel()
    elif rank_up():
      fusing = False
      i += 1
      cancel()
    else:
      open_25_familiars()
      select_all_fuse()
      
def script(key, fn):
  if data['script'] and data['script'][0] == key:
    data['script'] = None
    print("Stopping script:", key)
  else:
    print()
    print("Starting script:", key)
    data['script'] = (key, fn)

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio():
  pygame.mixer.music.load("images/ping.mp3")
  pygame.mixer.music.play()

def pause_audio():
  pygame.mixer.music.pause()

def press(key, delay=0.05):
  interception.key_down(key)
  time.sleep(delay)
  
def release(key, delay=0.05):
  interception.key_up(key)
  time.sleep(delay)

def press_release(key, delay=0.05):
  press(key)
  release(key, delay)

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

def reset_on_exception(fn):
  try:
    fn()
  except Exception as e:
    data['script'] = None
    clear()
    print(f"ERROR: {e}\n")
    commands()

def commands():
  print("Commands:")
  print(f"  {START_STOP_KEY} - start/stop")
  print("")
  print("PLEASE MAKE SURE YOUR MAPLESTORY IS IN 1920x1080!")

if __name__=="__main__":
  main()
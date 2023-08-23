# TODO: handle rare familiars, prob just use 50 at a time if possible when we are at 0/100 or 0/150, then proceed to commons as usual
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
      print()
      commands()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    stop_flag[0] = True

def fuse_familiars():
  res = pag.size()
  # Required locations
  fam_fusion_loc = pag.locateOnScreen(Images.FAM_FUSION, confidence=0.9, grayscale=True)
  if not fam_fusion_loc:
    raise Exception("Could not find familiar UI at the Collection -> Fusion tab")
  fam_equip_tab = pag.locateOnScreen(Images.FAM_EQUIP, confidence=0.9, grayscale=True)
  if not fam_equip_tab:
    raise Exception("Could not find inventory at the USE tab")

  # Regions
  fam_ui_region = (fam_fusion_loc.left, fam_fusion_loc.top, 750, 435)
  fam_ui_region_expanded = (fam_fusion_loc.left, fam_fusion_loc.top, min(1130, res[0] - fam_fusion_loc.left) , min(680, res[1] - fam_fusion_loc.top))
  fam_inventory_region = (fam_equip_tab.left, fam_equip_tab.top, min(675, res[0] - fam_equip_tab.left), min(390, res[1] - fam_equip_tab.top))

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
    interception.move_to(fam_locs[i].x, fam_locs[i].y)
    time.sleep(0.25)
    if pag.locateOnScreen(Images.FAM_STOP, confidence=0.9, grayscale=True, region=fam_ui_region_expanded):
      print("Found familiar to stop at")
      i = 100000
      return False
    if not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True, region=fam_ui_region_expanded):
      return False
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
    if not fam_select_all:
      fam_select_all = pag.locateCenterOnScreen(Images.FAM_SELECT_ALL, confidence=0.9, grayscale=True, region=fam_ui_region)
    if not fam_select_all:
      raise Exception("Could not find select all button")
    interception.click(fam_select_all, delay=0.25)
    if not fam_fuse:
      fam_fuse = pag.locateCenterOnScreen(Images.FAM_FUSE_ACTIVE, confidence=0.9, grayscale=True, region=fam_ui_region)
    if not fam_fuse:
      raise Exception("Could not find fuse button")
    while can_continue() and pag.locateOnScreen(Images.FAM_ASCENDION, confidence=0.9, grayscale=True, region=fam_ui_region):
      interception.click(fam_fuse)
      interception.click(fam_fuse, delay=0.25)
      if not can_continue(): break
      press_release("enter")
      press_release("enter")
      press_release("enter")
      time.sleep(0.25)

  def open_familiars():
    def find_stack(name, image, cache):
      nonlocal fam_inventory_region
      if name in cache: 
        return cache[name]
      cache[name] = pag.locateCenterOnScreen(image, region=fam_inventory_region)
      return cache[name] != None
  
    def find_exp_points(image):
      return pag.locateOnScreen(image, confidence=0.95, grayscale=True, region=fam_ui_region)
    
    def open(stackloc, amt):
      interception.click(stackloc)
      interception.click(stackloc)
      interception.click(stackloc)
      time.sleep(0.25)
      write(amt)
      if not can_continue(): return
      press_release("enter")
      press_release("enter")
      press_release("enter")
      time.sleep(0.25)

    def open_up_to(up_to_points):
      cache = { }
      order = [100, 75, 50, 25]
      steps = {
        150:  [ ("100 rare", Images.FAM_100_STACK_RARE, "75") ],
        100:  [ ("50 rare", Images.FAM_50_STACK_RARE, "50"), ("100 rare", Images.FAM_100_STACK_RARE, "50") ],
        75:   [ ("75 common", Images.FAM_75_STACK, "75"), ("100 common", Images.FAM_100_STACK, "75") ],
        50:   [ ("50 common", Images.FAM_50_STACK, "50"), ("75 common", Images.FAM_75_STACK, "50"), ("100 common", Images.FAM_100_STACK, "50") ],
        25:   [ ("25 common", Images.FAM_25_STACK, "25"), ("50 common", Images.FAM_50_STACK, "25"), ("75 common", Images.FAM_75_STACK, "25"), ("100 common", Images.FAM_100_STACK, "25") ]
      }
      for _, points_to_open in enumerate(order):
        if points_to_open > up_to_points:
          continue
        for item in steps[points_to_open]:
          name, image, amt = item
          if find_stack(name, image, cache):
            open(cache[name], amt)
            return
      raise Exception("Could not find 100, 75, 50, 25 familiar stacks to open in inventory")

    if find_exp_points(Images.FAM_0_150_POINTS):
      open_up_to(150)
    elif find_exp_points(Images.FAM_0_POINTS) or find_exp_points(Images.FAM_50_150_POINTS):
      open_up_to(100)
    elif find_exp_points(Images.FAM_25_POINTS) or find_exp_points(Images.FAM_75_150_POINTS):
      open_up_to(75)
    elif find_exp_points(Images.FAM_100_150_POINTS) or find_exp_points(Images.FAM_50_POINTS):
      open_up_to(50)
    else:
      open_up_to(25)
  
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
      if not can_continue(): return
      press_release("enter")
      press_release("enter")
      press_release("enter")
      time.sleep(0.25)
      # Check if familiar is level 1 so we know is rank up was successful
      interception.move_to(fam_hover)
      time.sleep(0.25)
      ranked_up = not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True, region=fam_ui_region)
      if ranked_up:
        time.sleep(6)
        print("Ranked up")
      else:
        print("Failed to rank up")
      return ranked_up
    return False
  
  i = 0
  while can_continue():
    if i >= len(fam_locs):
      print("Finished fusing familiars")
      data['script'] = None
      break
    
    # Look for a valid familiar to start fusing with
    if not fusing:
      if not check_if_valid():
        i += 1
        continue
      else:
        fusing = True
        interception.click(fam_locs[i].x, fam_locs[i].y, delay=0.5)
      
    # Open familiars, fuse, and try to rank up
    if rank_up():
      fusing = False
      i += 1
      cancel()
    else:
      open_familiars()
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

def write(word):
  for c in word:
    press_release(c)

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
  print("PLEASE MAKE SURE YOUR MAPLESTORY IS IN 1920x1080 (FULLSCREEN NOT NEEDED)!")

if __name__=="__main__":
  main()
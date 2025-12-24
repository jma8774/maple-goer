import time
import threading
import pygame
from datetime import datetime, timedelta
import pyautogui as pag
import os
from base import Images, Audio, KeyListener
import interception

EDIT_COMBINATIONS_KEY = 'f1'
START_CUBING_KEY = 'f2'
CUBE_TO_EPIC = 'f3'
FORCE_FIRST_CUBE = 'f4'

thread = None
combinations = []
data = {
  'stop_flag': False,
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
  kl = KeyListener(data)
  kl.add(EDIT_COMBINATIONS_KEY, lambda: script(edit_combinations.__name__, edit_combinations))
  kl.add(START_CUBING_KEY, lambda: script(cube.__name__, cube))
  kl.add(CUBE_TO_EPIC, lambda: script(cube.__name__, cube_to_epic))
  kl.add(FORCE_FIRST_CUBE, lambda: script(cube.__name__, lambda: cube(force_first=True)))
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
    data['stop_flag'] = True

def script(key, fn):
  if data['script'] and data['script'][0] == key:
    data['script'] = None
    clear()
    print_combinations()
    commands()
  else:
    print("Starting script:", key)
    data['script'] = (key, fn)

STATS = {
  "att":      { "display": "Attack",                "image": Images.ATTACK },
  "matt":     { "display": "Magic Attack",          "image": Images.MAGIC_ATTACk },
  "all":      { "display": "All Stat",              "image": Images.ALL },
  "str":      { "display": "STR",                   "image": Images.STR },
  "dex":      { "display": "DEX",                   "image": Images.DEX },
  "int":      { "display": "INT",                   "image": Images.INT },
  "luk":      { "display": "LUK",                   "image": Images.LUK },
  "critdmg":  { "display": "Critical Damage (don't use)",       "image": Images.CRIT_DMG }, # TODO: get the actual image
  "boss":     { "display": "Boss Damage",           "image": Images.BOSS },
  "ied":      { "display": "Ignore Enemy Defense",  "image": Images.IED },
  "meso":     { "display": "Meso Obtained",         "image": Images.MESO_OBTAINED }, # TODO: get the actual image
  "drop":     { "display": "Item Drop Rate",        "image": Images.ITEM_DROP }, # TODO: get the actual image
}

def print_combinations():
  print(f"Here are the lines we are looking for:")
  for i, combination in enumerate(combinations):
    display = ', '.join(sorted([f"{v}L {STATS[k]['display']}" for (k,v) in combination.items()], key=lambda x: x[3:]))
    print(f"  {i+1}. {display}")
  print(f"  {len(combinations)+1}.")
  print()
    
def edit_combinations():
  # TODO: Make a way to export/import combinations
  def parse_combination(comb):
    data = {}
    parts = comb.split(",")

    for part in parts:
      num, stat = part.split("-")
      num = int(num)
      stat = stat.lower()
      if stat not in STATS:
        raise Exception(f"Unsupported stat: {stat}")
      data[stat] = data[stat] + num if stat in data else num

    if sum(data.values()) > 3:
      raise Exception(f"Cannot have more than 3 lines of stat")
    return data

  global combinations
  MAIN = 0
  ENTER_COMBINATION = 1
  state = MAIN
  error = ""

  while data['script'] and data['script'][0] == edit_combinations.__name__:
    clear()
    if error:
      print(f"ERROR: {error}")
      error=""
    if state == MAIN:
      print_combinations()
      print("Commands:")
      print("  [add] - add combinations")
      print("  [<number>] - remove a combination")
      print("  [done] - finish editing combinations")
      cmd = input("Enter a command: ")
      if cmd == "add":
        state = ENTER_COMBINATION
      elif cmd.isdigit():
        index = int(cmd)
        if index > 0 and index <= len(combinations):
          combinations.pop(index-1)
      elif cmd == "done":
        data['script'] = None
        clear()
        print_combinations()
        commands()
    elif state == ENTER_COMBINATION:
      print_combinations()
      print("You can enter the number of lines you want for a certain stat (eg. '2-all' for 2 lines of all stat, '1-att' for 1 line of attack, '3-dex' for 3 lines of dex)")
      print("If you want multiple stats, separate them with a comma (eg. '1-all,1-dex' for 1 line of all stat and 1 line of dex)")
      print("Supported Lines:")
      for k, v in STATS.items():
        print(f"  {k.ljust(8)} - {v['display']}")

      print()
      print("Commands:")
      print("  [<combination>] - add a combination")
      print("  [done] - finish adding combinations")
      cmd = input("Enter a command: ")
      if cmd == "done":
        state = MAIN
      else:
        try:
          combinations.append(parse_combination(cmd))
        except Exception as e:
          error = e;

def refresh_mouse_position():
  data['corner_pos'] = pag.locateOnScreen(Images.CUBE_POTENTIAL_KEYWORD_TOPLEFT, confidence=0.7, grayscale=True)
  print(f"Top left corner of the inner cube ui box is at: {data['corner_pos']}")

def cube_to_epic():
  cube(tier_to=Images.EPIC_POT)

def cube(tier_to=None, force_first=False):
  refresh_mouse_position()
  if not data['corner_pos']:
    raise Exception("Can't find cubing ui box, exiting...")

  try_again_loc = None
  def try_again():
    # press_release('enter', delay=0.1)
    # press_release('enter', delay=0.1)
    # nonlocal try_again_loc
    # if not try_again_loc:
    #   interception.move_to((200,200))
    #   try_again_loc = pag.locateOnScreen(Images.POTENTIAL_RESET_KEYWORD, confidence=0.8, grayscale=True) or
    # if not try_again_loc:
    #   raise Exception("One more try not found, exiting...")
    # interception.click(try_again_loc)
    # press_release('enter', delay=0.1)
    # press_release('enter', delay=0.1)
    # press_release('enter', delay=0.1)
    # press_release('enter', delay=0.1)
    press_release('space', delay=0.2)
    press_release('space', delay=0.2)
    press_release('space', delay=0.2)

  lines_found = {}
  for combination in combinations:
    for stat in combination.keys():
      lines_found[stat] = 0

  def check_for_lines():
    nonlocal force_first
    if force_first:
      print("Forcing first cube...")
      force_first = False
      return False
    for stat in lines_found:
      locs = pag.locateAllOnScreen(STATS[stat]["image"], confidence=0.95, region=box_region)
      lines_found[stat] = len(list(locs)) if locs else 0
      print(f"{stat}: {lines_found[stat]}")

    for combination in combinations:
      good = True
      for stat, required_amt in combination.items():
        if lines_found[stat] < required_amt:
          good = False
          break
      if good:
        return True
    return True if len(combination) == 0 else False
  
  def check_for_tier():
    print("Checking for tier up...")
    return pag.locateOnScreen(tier_to, confidence=0.8, grayscale=True, region=box_region)
  
  # width = 1203-819
  # height = 714-608
  width = 1203-819
  height = 714-608
  box_region = (data['corner_pos'][0]-15, data['corner_pos'][1], width, height)
  ok_loc = None
  while data['script'] and data['script'][0] == cube.__name__:
    if (not tier_to and not check_for_lines()) or (tier_to and not check_for_tier()):
      # ok_loc = pag.locateOnScreen(Images.OK_START, confidence=0.8, grayscale=True, region=box_region)
      # if ok_loc:
      #   interception.click(ok_loc, delay=0.1)
      try_again()
    else:
      print("Desired lines found, cubing stopped.")
      play_audio()
      data['script'] = None
      break
    time.sleep(1.1)
    # now = datetime.now()
    # while not pag.locateOnScreen(Images.ATT_INCREASE, confidence=0.8, grayscale=True, region=box_region):
    #   time.sleep(0.1)
    #   if datetime.now() - now > timedelta(seconds=1.5):
    #     print("Bugged")
    #     play_audio("images/retro_ping.wav", 1)
    #     now = datetime.now() + timedelta(seconds=9999)

def setup_audio(volume=1):
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.set_volume(volume)

def play_audio(song="images/ping.mp3", loops=1):
  pygame.mixer.music.load(song)
  pygame.mixer.music.play(loops=loops)

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
  print(f"  {EDIT_COMBINATIONS_KEY} - edit stat combinations to stop at")
  print(f"  {START_CUBING_KEY} - start/stop cubing")
  print(f"  {CUBE_TO_EPIC} - start/stop cubing to epic")
  print(f"  {FORCE_FIRST_CUBE} - force first cube")
  print("")
  print("PLEASE MAKE SURE YOUR MAPLESTORY IS IN 1920x1080!")
  print("TO TEST IF THE CUBING WORKS ON YOUR MAPLESTORY, TRY AN EASY COMBINATION LIKE 1L OF ATTACK AND SEE IF IT STOPS!")

if __name__=="__main__":
  main()
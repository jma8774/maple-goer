import pyautogui as pag
import time
from datetime import datetime, timedelta
import threading
from base import Images, Audio, KeyListener, shutdown_computer
Images = Images.POE
import pyautogui as pag
import interception as it
import pygame
import sys
from collections import deque
from win32gui import GetWindowText, GetForegroundWindow
import pyperclip as pc
from item_parser.line import Line
from item_parser.item import Item
from item_parser.configs.affix_config import AffixConfig
from item_parser.constants import Operator
from item_parser.configs.item_base_config import ConfigsModule, Config
from item_parser.work_item import CraftingWorkItem
from random import randint
from PIL import Image
import traceback

class Scripts:
  def __init__(self, obj):
    for (key, value) in obj.items():
      setattr(self, key, value)

# Hotkeys
AUTO_SOMETHING_KEY = 'f1'
CRAFT_CHAOS_SPAM_KEY = 'f2'
CRAFT_MAPS_KEY = 'f4'
CRAFT_FROM_QUEUE_TAB_KEY = 'f7'
CANCEL_KEY = 'f12'


# Data
scripts = None
data = {
  "stop_flag": False,
  "target": None,
  "cmd": {}
}

# Locations
LOCATIONS = {
  "showcase": (440, 625),
  "tl_corner_inventory": (1725, 805),
  "chat_x_button": (1805, 558)
}

# Currency Locations - Currency Tab
CURRENCY_LOCATIONS = {
  "alt": (145, 360),
  "aug": (305, 435),
  "regal": (579, 362)
}
INACTIVE_CURRENCY_IMGS = {
  "transmute": Images.inactive_transmute,
  "alt": Images.inactive_alt,
  "aug": Images.inactive_aug,
  "regal": Images.inactive_regal,
  "scour": Images.inactive_scour,
  "exalt": Images.inactive_exalt,
  "annul": Images.inactive_annul,
  "chaos": Images.inactive_chaos,
}
CACHED_REGIONS = {
  "transmuate": None,
  "alt": None,
  "aug": None,
  "regal": None,
  "scour": None,
  "exalt": None,
  "annul": None,
  "chaos": None
}

# Areas (x, y, width, height)
REGION = {
  "stash": (0, 0, 870, 1150),
  "stash_currency_bottom": (175, 775, 715-175, 925-775),
  "inventory": (1685, 775, 2554-1685, 1150-775),
  "showcase_item_name": (0, 0, 1300, 475),
  "highlight_showcase": (380, 700, 509-380, 732-700),
  "managlobe40": (2363, 1316, 2405-2363, 1340-1316),
  "hpglobe60": (151, 1257, 169-151, 1272-1257),
  "managlobe40wide": (2390, 1160, 2416-2390, 1200-1160),
  "managlobe40widefs": (2390, 968, 2416-2390, 1008-968),
  "hpglobe60wide": (150, 1100, 173-150, 1122-1100),
  "hpglobe60widefs": (150, 900, 173-150, 940-900),
  "showcase_box": (415, 575, 461-415, 624-575),
  "chat": (875, 400, 1845-875, 595-400)
}
INVENTORY_COORDS = [
  [(1730+(x*70), 820) for x in range(12)],
  [(1730+(x*70), 890) for x in range(12)],
  [(1730+(x*70), 960) for x in range(12)],
  [(1730+(x*70), 1030) for x in range(12)],
  [(1730+(x*70), 1100) for x in range(12)]
]
STASH_CORDS = [
  [(55+(x*70), 200) for x in range(12)],
  [(55+(x*70), 270) for x in range(12)],
  [(55+(x*70), 340) for x in range(12)],
  [(55+(x*70), 410) for x in range(12)],
  [(55+(x*70), 480) for x in range(12)],
  [(55+(x*70), 550) for x in range(12)],
  [(55+(x*70), 620) for x in range(12)],
  [(55+(x*70), 690) for x in range(12)],
  [(55+(x*70), 760) for x in range(12)],
  [(55+(x*70), 830) for x in range(12)],
  [(55+(x*70), 900) for x in range(12)],
  [(55+(x*70), 970) for x in range(12)]
]
TABS = {
  "dump": (975, 150),
  "queue": (975, 180),
  "currency": (975, 240),
}

def raise_and_stop(msg):
  data["target"] = None
  raise Exception(msg)

def test():
  print("Testing item parser...")
  try:
    item = Item(pc.paste())
    item_config = ConfigsModule.get_config_by_base_name(item)
    print(f"is_valid={is_valid(item, item_config)}")
    print()
  except Exception as e:
    print("Item parser test failed: ", e)
    traceback.print_exception(type(e), e, e.__traceback__)
    print(pc.paste())
    print()

def main():
  test()
  setup_audio(volume=0.5)  

  # Interception Setup for main loop
  kdevice = it.listen_to_keyboard()
  mdevice = it.listen_to_mouse()
  it.inputs.keyboard = kdevice
  it.inputs.mouse = mdevice

  # Interception Key Listener Setup (seperate thread)
  global scripts
  scripts = Scripts({
  "CraftChaosSpam": {
    "name": "Craft chaos spam",
    "fn": craft_chaos_spam
  },
  "CraftMaps": {
    "name": "Craft maps",
    "fn": craft_maps
  },
  "CraftFromQueueTab": {
    "name": "Craft from queue tab",
    "fn": craft_from_queue_tab
  },
  "AutoSomething": {
    "name": "Auto Something",
    "fn": auto_pf
  },
})
  kl = KeyListener(data)
  # kl.add(CRAFT_MAPS_KEY, lambda: toggleScript(scripts.CraftMaps))
  kl.add(CRAFT_CHAOS_SPAM_KEY, lambda: toggleScript(scripts.CraftChaosSpam))
  kl.add(CRAFT_FROM_QUEUE_TAB_KEY, lambda: toggleScript(scripts.CraftFromQueueTab))
  kl.add(AUTO_SOMETHING_KEY, lambda: toggleScript(scripts.AutoSomething))
  kl.add(CANCEL_KEY, cancel)
  kl.run()

  for arg in sys.argv[1:]: # shutdownwhendone
    key, value = arg.split("=")
    data["cmd"][key] = value

  print("\nArguments:", sys.argv[1:])
  commands()
  try:
    while True:
      while data["target"] == None: 
        time.sleep(1)
        continue
      thread = threading.Thread(target=lambda: data["target"]["fn"](data["target"]))
      thread.start()
      thread.join()
      commands()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    data['stop_flag'] = True

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(
            f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

def cancel():
  global data
  data["target"] = None
  print("All scripts stopped")

def auto_pf(scriptobj):
  # it's actually 20%
  def mana_more_than_40():
    return pag.locateOnScreen(Images.mana40wide, confidence=0.8, grayscale=True, region=REGION["managlobe40widefs"])
  
  def hp_more_than_60():
    return pag.locateOnScreen(Images.hp60wide, confidence=0.8, grayscale=True, region=REGION["hpglobe60widefs"])
  
  mana_cd = datetime.now()
  hp_cd = datetime.now()
  hp_interval_cd = datetime.now()
  phase_run_cd = datetime.now()
  cd_2 = datetime.now()
  cd_3 = datetime.now()
  cd_4 = datetime.now()
  cd_5 = datetime.now()
  vaal_haste_cd = datetime.now()
  blessing_cd = datetime.now()
  leftbracket_cd = datetime.now()
  rightbracket_cd = datetime.now()
  semicolon_cd = datetime.now()
  singlequote_cd = datetime.now()
  while data["target"] == scriptobj:  
    if GetWindowText(GetForegroundWindow()) == "Path of Exile":
      now = datetime.now()
      # if now > mana_cd and not mana_more_than_40():
      #   print("Potted MP!")
      #   press_release("5")
      #   mana_cd = datetime.now() + timedelta(seconds=2)
      if now > cd_2:
        press_release("2")
        cd_2 = datetime.now() + timedelta(seconds=4)
      # if now > cd_3:
      #   press_release("3")
      #   cd_3 = datetime.now() + timedelta(seconds=11.5)
      # if now > cd_4:
      #   press_release("4")
      #   cd_4 = datetime.now() + timedelta(seconds=15)
      # if now > cd_5:
      #   press_release("5")
      #   cd_5 = datetime.now() + timedelta(seconds=9)
      # healbecausehpislow = now > hp_cd and not hp_more_than_60()
      # # if healbecausehpislow or now > hp_interval_cd:
      # if healbecausehpislow:
      #   # print("Potted HP!")
      #   press_release("1", 0, 0.1)
      #   if healbecausehpislow:
      #     hp_cd = datetime.now() + timedelta(seconds=0.5)
        # hp_interval_cd = datetime.now() + timedelta(seconds=3.4)
      # if now > phase_run_cd:
      #   # print("Phase Run!")
      #   press_release("r")
      #   phase_run_cd = datetime.now() + timedelta(seconds=4)
      if now > blessing_cd:
        # print("Blessing!")
        press_release("r", 0, 0.1)
        blessing_cd = datetime.now() + timedelta(seconds=16)
      if now > vaal_haste_cd:
        # print("Vaal Haste!")
        press_release("t", 0, 0.01)
        vaal_haste_cd = datetime.now() + timedelta(seconds=4)
      if now > leftbracket_cd:
        press_release("[")
        leftbracket_cd = datetime.now() + timedelta(seconds=12.2)
      if now > rightbracket_cd:
        press_release("]", 0, 0.01) 
        rightbracket_cd = datetime.now() + timedelta(seconds=4.3)
      if now > semicolon_cd:
        press_release(";", 0, 0.01)
        semicolon_cd = datetime.now() + timedelta(seconds=17)
      if now > singlequote_cd:
        press_release("'", 0, 0.01)
        singlequote_cd = datetime.now() + timedelta(seconds=5.7)
      time.sleep(0.2)
      if data["target"] != scriptobj:
        break
  data["target"] = None
  
def craft_chaos_spam(scriptobj):
  while data["target"] == scriptobj:
    pick_up_by_name("chaos")
    press('ctrl')
    press('altleft')
    press('shift')
    moveto_flicker(LOCATIONS["showcase"], delay=0.05)
    item = safe_copy_item(Item.get_default())
    item_config = ConfigsModule.get_config_by_base_name(item)
    while not is_valid(item, item_config):
      click()
      item = safe_copy_item(item)
      if data["target"] != scriptobj:
        break
    double_release(["ctrl", "shift", "altleft"])
  

def perform_actions_until_different_item(item: Item, actions: list):
  new_item = safe_copy_item(item)
  while new_item == item:
    print("Same item! Performing actions...")
    for action in actions:
      action()
    new_item = safe_copy_item(item)
  return new_item

def safe_copy_item(current_item: Item):
  new_item = current_item
  n = 70
  while n > 0:
    press_release('c', delay=0, pressdelay=0.01)
    try:
      new_item = Item(pc.paste())
    except Exception as e:
      raise_and_stop(f"[safe_copy_item] Item parser failed: {e}")
    if current_item != new_item:
      return new_item
    time.sleep(0.005)
    n -= 1
  return new_item

def is_valid(item: Item, item_config: Config):
  print(item)
  if item is None:
    raise_and_stop("Item is None")
  
  total_required = item_config.get("num_affixes_required")
  if total_required == 0 or total_required is None:
    raise_and_stop("No affixes required (1)")
  
  if len(item_config.get("prefixes")) == 0 and len(item_config.get("suffixes")) == 0:
    raise_and_stop("No affixes to check (2)")

  if item_config.get("custom_is_valid_pre") is not None and item_config.get("custom_is_valid_pre")(item):
    return True
  
  prefixes = ConfigsModule.good_prefixes(item, item_config)
  suffixes = ConfigsModule.good_suffixes(item, item_config)
  # print(f"prefixes={prefixes}, suffixes={suffixes}, total_required={total_required}")
  if prefixes + suffixes < total_required:
    return False
  
  # Certain configs can apply special checks as a last resort
  if item_config.get("custom_is_valid") is None:
    return True
  return item_config.get("custom_is_valid")(item)
  
def make_all_inventory_queue():
  queue = deque([(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (0,10), (0,11), \
                 (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), \
                 (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), \
                 (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), \
                 (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11)])
  return queue

def craft_from_queue_tab(scriptobj):
  def refill_inventory_from_queue():
    moveto(TABS["queue"], 0.1)
    click()
    click()
    press('ctrl', 0.1)
    for r in range(12):
      for c in range(12):
        moveto(STASH_CORDS[c][r])
        click()
        click()
        if data["target"] != scriptobj:
          break
      if data["target"] != scriptobj:
        break
    # Leave the back of the inventory open so we can return the item to the dump tab (make a 2x4 space in the back)
    press('shift', 0.1)
    queue = [INVENTORY_COORDS[0][10], INVENTORY_COORDS[0][11], INVENTORY_COORDS[1][10], INVENTORY_COORDS[1][11], INVENTORY_COORDS[2][10], INVENTORY_COORDS[2][11], INVENTORY_COORDS[3][10], INVENTORY_COORDS[3][11]]
    for loc in queue:
      if data["target"] != scriptobj:
        break
      moveto(loc)
      click()
      click()
    release('shift')
    release('ctrl', 0.1)
  
  number_of_fully_empty_cycles = 0
  while data["target"] == scriptobj:
    queue = make_all_inventory_queue()
    workitem = CraftingWorkItem(queue)
    empty_slots = crafting(scriptobj, workitem, resetscript=False)
    if empty_slots == 60: 
      number_of_fully_empty_cycles += 1
      if number_of_fully_empty_cycles >= 5: 
        data["target"] = None
        if "shutdownwhendone" in data["cmd"]:
          shutdown_computer()
    if data["target"] != scriptobj: break
    refill_inventory_from_queue()
    if data["target"] != scriptobj: break
    move_back_to_currency_tab()

def crafting(scriptobj, workitem: CraftingWorkItem, resetscript=True):
  queue = deque(workitem.positions)
  empty_slots = 0
  while len(queue) > 0:
    try_close_chat()
    current = queue.popleft()
    print(f"Placing item from inventory {current}")
    place_item(current)
    if data["target"] != scriptobj: break
    if pag.locateOnScreen(Images.showcase_empty, grayscale=True, confidence=0.8, region=REGION["showcase_box"]):
      print("Showcase empty, going to the next one...")
      empty_slots += 1
      continue
    try:
      pick_up_by_name("alt")
      press('ctrl')
      press('altleft')
      press('shift')
      moveto_flicker(LOCATIONS["showcase"], delay=0.05)
      item = safe_copy_item(Item.get_default())
      item_config = ConfigsModule.get_config_by_base_name(item)
    except Exception as e:
      print(f"Item parser failed: {e}")
      double_release(["ctrl", "shift", "altleft"])
      return_item()
      dump_tab_it()
      move_back_to_currency_tab()
      continue

    same_item_seq = 0
    num_affixes_required = item_config.get("num_affixes_required")
    # time_since_last_close_chat = datetime.now()
    while not is_valid(item, item_config):
      start_item = item
      # Scour and transmute if we have a rare item
      pick_up_alt = item.rarity == "Rare" or item.rarity == "Normal"
      if item.rarity == "Rare":
        scour_it()
        transmute_it()
      elif item.rarity == "Normal":
        transmute_it()

      if pick_up_alt:
        time.sleep(0.3)
        pick_up_by_name("alt")
        press('shift')
        moveto(LOCATIONS["showcase"], delay=0.2)

      click(delay=0)
      item = safe_copy_item(item)

      # Augment if we have less than 2 affixes and we have a good prefix or suffix
      augged = False
      if num_affixes_required >= 2 and len(item.affixes) < 2 and (ConfigsModule.good_prefixes(item, item_config) + ConfigsModule.good_suffixes(item, item_config) >= 1):
        augged = True
        print("\n💎 Augging!")
        aug_it()
        item = perform_actions_until_different_item(item, [try_close_chat, aug_it])
        print(item)

      # Regal if we have less than 3 affixes and we have 2 good prefixes or suffixes
      regaled = False
      custom_should_regal = item_config.get("custom_should_regal")
      if num_affixes_required >= 3 and len(item.affixes) < 3 and ((custom_should_regal and custom_should_regal(item)) or (not custom_should_regal and ConfigsModule.good_prefixes(item, item_config) + ConfigsModule.good_suffixes(item, item_config) >= 2)):
        regaled = True
        print("\n💎 Regaling!")
        regal_it()
        item = perform_actions_until_different_item(item, [try_close_chat, regal_it])
        print(item)

      custom_should_exalt = item_config.get("custom_should_exalt")
      if regaled and custom_should_exalt is not None and custom_should_exalt(item):
        print("Exalting since custom_should_exalt check passed")
        print("\n💎 Exalting!")
        play_audio("images/retro_ping.wav", 1)
        exalt_it()
        item = perform_actions_until_different_item(item, [try_close_chat, exalt_it])
        print(item)
        while not is_valid(item, item_config):
          print("\n💎 Annuling!")
          annul_it()
          item = perform_actions_until_different_item(item, [try_close_chat, annul_it])
          print(item)
          if item_config.get("custom_should_exalt") is not None and item_config.get("custom_should_exalt")(item):
            print("\n💎 Exalting again!")
            exalt_it()
            item = perform_actions_until_different_item(item, [try_close_chat, exalt_it])
            print(item)
          else:
            break

      if augged:
        pick_up_by_name("alt")
        press('shift')
        moveto(LOCATIONS["showcase"], delay=0.06)
      same_item_seq = same_item_seq + 1 if start_item == item else 0
      if same_item_seq >= 10:
        print("Same item sequence reached 10, breaking, this either means we bug out or we ran out of currencies to use...")
        # if "shutdownwhendone" in data["cmd"]:
        #   shutdown_computer()
        double_release(["ctrl", "shift", "altleft"])
        time.sleep(0.5)
        break
      if data["target"] != scriptobj: break

    double_release(["ctrl", "shift", "altleft"])
    try_close_chat()
    if data["target"] == scriptobj: 
      play_audio()
      return_item()
      # Move it to the dump tab
      dump_tab_it()
      # Move back to currency tab
      move_back_to_currency_tab()
    else:
      break

  if resetscript:
    data["target"] = None
  return empty_slots

def craft_maps(scriptobj):
  press('ctrl', 0.05)
  press('shift', 0.05)
  press('altleft', 0.05)
  pick_up_by_name("chaos")
  press('shift', 0.05)
  for r in range(12):
    for c in range(12):
      if data["target"] != scriptobj:
        break
      moveto(STASH_CORDS[r][c], 0.05)
      try:
        item = safe_copy_item(Item.get_default())
        print(item)
        if item.is_corrupted or item.type != "Maps":
          continue
        item_config: Config = ConfigsModule.get_config_by_base_name(item)
      except Exception as e:
        print(f"Item parser failed: {e}")
        continue
      while not is_valid(item, item_config):
        click()
        item = safe_copy_item(item)
        if data["target"] != scriptobj:
          break
      if data["target"] != scriptobj:
        break
    if data["target"] != scriptobj:
      break

def attack_and_vaal_haste(scriptobj):
  def can_vaal_haste(now): return last_vaal_haste + timedelta(seconds=8) < now
  def can_sigil(now): return last_sigil + timedelta(seconds=11) < now

  last_vaal_haste = datetime.now() - timedelta(seconds=99)
  last_sigil = datetime.now() - timedelta(seconds=99)
  while data["target"] == scriptobj:
    now = datetime.now()
    if can_vaal_haste(now):
      press_release("r", 0.15 if can_sigil(now) else 0)
      last_vaal_haste = datetime.now()
    if can_sigil(now):
      press_release("e")
      last_sigil = datetime.now()
    press("w")
    while (datetime.now() - now).seconds < 3:
      time.sleep(0.25)
      if data["target"] != scriptobj:
        break
    release("w")

def place_item(pos):
  x, y = pos
  moveto(INVENTORY_COORDS[x][y], delay=0.1)
  press('ctrl')
  press('shift')
  click()
  click()
  double_release(["shift", "ctrl"])
  time.sleep(0.05)

def try_close_chat():
  moveto((0,0))
  while pag.locateOnScreen(Images.chat_local_tab, grayscale=True, confidence=0.8, region=REGION["chat"]):
    loc = pag.locateOnScreen(Images.poe_window_x, grayscale=True, confidence=0.8, region=REGION["chat"])
    if loc is None:
      loc = (1805, 558)
    click(loc)

# We have a 2x4 space in the back of the inventory, we can return the item to the dump tab
def return_item():
  release('shift', 0.01)
  release('shift', 0.01)
  moveto(LOCATIONS["showcase"], 0.1)
  click()
  moveto(INVENTORY_COORDS[0][11], 0.1)
  click()

def dump_tab_it():
  moveto(TABS["dump"], 0.2)
  click()
  click()
  moveto(INVENTORY_COORDS[0][11], 0.2)
  press('shift')
  press('ctrl', 0.2)
  click()
  click()
  release('shift')
  release('ctrl')

def move_back_to_currency_tab():
  moveto(TABS["currency"], 0.1)
  click()
  click()
  
def use_it(currency):
  release('shift', delay=0)
  release('shift', delay=0.01)
  pick_up_by_name(currency)
  x, y = LOCATIONS["showcase"]
  moveto((x+5, y+5), delay=0)
  moveto((x-5,y-5), delay=0.01)
  moveto((x-5,y+5), delay=0.01)
  moveto((x,y), delay=0.03)
  click(delay=0.05)

def alt_it():
  use_it("alt")

def aug_it():
  use_it("aug")

def regal_it(): 
  use_it("regal")

def exalt_it():
  use_it("exalt")

def transmute_it():
  use_it("transmute")

def scour_it():
  use_it("scour")

def annul_it():
  use_it("annul")

def pick_up(name):
  release('shift')
  moveto(CURRENCY_LOCATIONS[name])
  right_click()
  
def get_image_location(cachekey, img):
  if cachekey not in CACHED_REGIONS or CACHED_REGIONS[cachekey] is None:
    CACHED_REGIONS[cachekey] = REGION["stash"]
  # moveto((randint(510, 540), randint(490, 725)), delay=0)
  loc = pag.locateOnScreen(img, confidence=0.85, grayscale=True, region=CACHED_REGIONS[cachekey]) or pag.locateOnScreen(img, confidence=0.85, grayscale=True, region=REGION["stash"]) or pag.locateOnScreen(img, confidence=0.85, grayscale=True)
  if not loc:
    print(f"Image not found, moving mouse away")
    moveto((randint(0, 2400), randint(0, 115)), delay=0.1)
    loc = pag.locateOnScreen(img, confidence=0.85, grayscale=True, region=CACHED_REGIONS[cachekey]) or pag.locateOnScreen(img, confidence=0.85, grayscale=True, region=REGION["stash"]) or pag.locateOnScreen(img, confidence=0.85, grayscale=True)
  if not loc:
    raise_and_stop(f"Image not found on screen")
  x, y = loc.left, loc.top
  CACHED_REGIONS[cachekey] = (x-loc.width, y-loc.height, loc.width*3, loc.height*3)
  # print(CACHED_REGIONS[cachekey])
  return loc

# I have more than 2 stacks of alts > 5000 quantity, they're in different coordinates
def pick_up_by_name(name: str):
  release('shift', delay=0)
  release('shift', delay=0.01)
  try:
    img = INACTIVE_CURRENCY_IMGS[name]
  except Exception as e:
    raise_and_stop(f"Invalid currency name: {name}")
  loc = get_image_location(name, img)
  moveto((loc.left+5, loc.top+5), delay=0)
  moveto((loc.left-5, loc.top-5), delay=0)
  moveto((loc.left-5, loc.top+5), delay=0.01)
  moveto(loc, delay=0.05)
  right_click(delay=0.05)
  
def highlight():
  return pag.locateOnScreen(Images.highlight, confidence=0.8, grayscale=True, region=REGION["highlight_showcase"])

def toggleScript(scriptObj):
  if data["target"] is not None and data["target"] != scriptObj:
    print("Stopping previously running script before starting...")
  data["target"] = None if data["target"] == scriptObj else scriptObj
  if data["target"] == scriptObj:
    print(f"\nStart {scriptObj['name']}")
  else:
    print(f"Stop {scriptObj['name']}")

def double_release(keys):
  for key in keys:
    release(key)
    release(key)

def click(location=None, delay=0.05):
  if (location == None):
    it.click()
  else:
    it.click(location)
  if delay > 0:
    time.sleep(delay)

def right_click(location=None, delay=0.05):
  if (location == None):
    it.right_click()
  else:
    it.right_click(location)
  if delay > 0:
    time.sleep(delay)

def moveto_flicker(location, delay=0.05):
  moveto((location[0]+5, location[1]+5), delay=0)
  moveto((location[0]-5, location[1]-5), delay=0)
  moveto(location, delay=0)
  if delay > 0:
    time.sleep(delay)
    
def moveto(location, delay=0.05):
  it.move_to(location)
  if delay > 0:
    time.sleep(delay)

def doubleclick(location, delay=0.05):
  it.click(location)
  time.sleep(0.02)
  it.click(location)
  time.sleep(delay)

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
  it.key_down(key)
  if delay > 0:
    time.sleep(delay)
  
def release(key, delay=0.05):
  it.key_up(key)
  if delay > 0:
    time.sleep(delay)

def press_release(key, delay=0.05, pressdelay=0.05):
  press(key, pressdelay)
  release(key, delay)

def commands():
  print("Commands:")
  # print(f"\t{CRAFT_MAPS_KEY} - start/end craft maps")
  print(f"\t{AUTO_SOMETHING_KEY} - start/end auto something")
  print(f"\t{CRAFT_CHAOS_SPAM_KEY} - start/end craft chaos spam")
  print(f"\t{CRAFT_FROM_QUEUE_TAB_KEY} - start/end craft from queue tab")
  print(f"\t{CANCEL_KEY} - cancel all scripts")

if __name__=="__main__":
  main()
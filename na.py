import pyautogui as pag
import time
from datetime import datetime, timedelta
import threading
from base import Images, Audio, KeyListener
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
from item_parser.configs.item_base_config import BaseItemConfig
from item_parser.work_item import CraftingWorkItem
from random import randint

class Scripts:
  def __init__(self, obj):
    for (key, value) in obj.items():
      setattr(self, key, value)

# Hotkeys
CRAFTING_1x2_KEY = 'f1'
CRAFTING_2x4_KEY = 'f2'
CRATING_1x1_KEY = 'f3'
CRAFT_UNTIL_HIGHLIGHT_KEY = 'f4'
PRESS_E_EVERY_INTERVAL_KEY = 'f6'
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
  "tl_corner_inventory": (1725, 805)
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
}

# Areas (x, y, width, height)
REGION = {
  "stash": (0, 0, 870, 1150),
  "inventory": (1685, 775, 2554-1685, 1150-775),
  "showcase_item_name": (0, 0, 1300, 475),
  "highlight_showcase": (380, 700, 509-380, 732-700),
  "managlobe40": (2363, 1316, 2405-2363, 1340-1316),
  "hpglobe60": (151, 1257, 169-151, 1272-1257),
  "showcase_box": (415, 575, 461-415, 624-575)
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

def test():
  print("Testing item parser...")
  try:
    item = Item(pc.paste())
    item_config = BaseItemConfig.get_config_by_base_name(item)
    print(f"is_valid={is_valid(item, item_config)}")
    print()
  except Exception as e:
    print("Item parser test failed: ", e)
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
  "Crafting_1x2": {
    "name": "Crafting 1x2 Items",
    "fn": crafting_1x2,
  },
  "Crafting_2x4": {
    "name": "Crafting 2x4 Items",
    "fn": crafting_2x4
  },
  "Crafting_1x1": {
    "name": "Crafting 1x1 Items",
    "fn": crafting_1x1
  },
  "CraftUntilHighlight": {
    "name": "Craft until highlight",
    "fn": craft_until_highlight
  },
  "CraftFromQueueTab": {
    "name": "Craft from queue tab",
    "fn": craft_from_queue_tab
  },
  "AutoVaalHaste": {
    "name": "Auto Vaal Haste",
    "fn": auto_vaal_haste
  },
})
  kl = KeyListener(data)
  kl.add(CRAFTING_1x2_KEY, lambda: toggleScript(scripts.Crafting_1x2))
  kl.add(CRAFTING_2x4_KEY, lambda: toggleScript(scripts.Crafting_2x4))
  kl.add(CRATING_1x1_KEY, lambda: toggleScript(scripts.Crafting_1x1))
  kl.add(CRAFT_UNTIL_HIGHLIGHT_KEY, lambda: toggleScript(scripts.CraftUntilHighlight))
  kl.add(CRAFT_FROM_QUEUE_TAB_KEY, lambda: toggleScript(scripts.CraftFromQueueTab))
  kl.add(PRESS_E_EVERY_INTERVAL_KEY, lambda: toggleScript(scripts.AutoVaalHaste))
  kl.add(CANCEL_KEY, cancel)
  kl.run()

  # highlight=bow for crafting all bows in your inventory until you find a good one
  for arg in sys.argv[1:]:
    print(arg)
    print(arg.split("="))
    key, value = arg.split("=")
    data["cmd"][key] = value

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

def auto_vaal_haste(scriptobj):
  while data["target"] == scriptobj:
    if GetWindowText(GetForegroundWindow()) == "Path of Exile":
        press_release("r")
    time.sleep(3)
    if data["target"] != scriptobj:
      break
    
def auto_pot(scripts):
  def mana_more_than_40():
    return pag.locateOnScreen(Images.mana40, confidence=0.7, grayscale=True, region=REGION["managlobe40"])
  
  def hp_more_than_60():
    return pag.locateOnScreen(Images.hp60, confidence=0.8, grayscale=True, region=REGION["hpglobe60"])
  
  mana_cd = datetime.now()
  hp_cd = datetime.now()
  while data["target"] == scripts.AutoPot:
    if GetWindowText(GetForegroundWindow()) == "Path of Exile":
      now = datetime.now()
      # if now > mana_cd and not mana_more_than_40():
      #   print("Potted MP!")
      #   press_release("2")
      #   mana_cd = datetime.now() + timedelta(seconds=2)
      if now > hp_cd and not hp_more_than_60():
        print("Potted HP!")
        press_release("1")
        hp_cd = datetime.now() + timedelta(seconds=2)
    time.sleep(0.25)
    if data["target"] != scripts.AutoPot:
      break
  data["target"] = None

def safe_copy_item(current_item: Item):
  new_item = current_item
  n = 20
  while n > 0:
    press_release('c', delay=0, pressdelay=0.01)
    new_item = Item(pc.paste())
    if current_item != new_item:
      return new_item
    time.sleep(0.02)
    n -= 1
  return new_item

def good_prefixes(item: Item, item_config: BaseItemConfig):
  good_prefixes: list[AffixConfig] = item_config.get("prefixes")
  if len(good_prefixes) == 0:
    return 0
  num_good = 0
  for p in good_prefixes:
    if item.affixes.get(p._affix_name) and p.pass_check(item.affixes.get(p._affix_name)):
      num_good += 1
  return num_good

def good_suffixes(item: Item, item_config: BaseItemConfig):
  good_suffixes: list[AffixConfig] = item_config.get("suffixes")
  if len(good_suffixes) == 0:
    return 0
  num_good = 0
  for s in good_suffixes:
    if item.affixes.get(s._affix_name) and s.pass_check(item.affixes.get(s._affix_name)):
      num_good += 1
  return num_good 

def is_valid(item: Item, item_config: BaseItemConfig):
  print(item)
  if item is None:
    raise Exception("Item is None")
  
  total_required = item_config.get("num_affixes_required")
  if total_required == 0 or total_required is None:
    raise Exception("No affixes required (1)")
  
  if len(item_config.get("prefixes")) == 0 and len(item_config.get("suffixes")) == 0:
    raise Exception("No affixes to check (2)")
  
  prefixes = good_prefixes(item, item_config)
  suffixes = good_suffixes(item, item_config)
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
    for i in range(12):
      for j in range(12):
        moveto(STASH_CORDS[i][j])
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
  
  while data["target"] == scriptobj:
    queue = make_all_inventory_queue()
    workitem = CraftingWorkItem(queue)
    crafting(scriptobj, workitem, resetscript=False)
    if data["target"] != scriptobj:
      break
    refill_inventory_from_queue()
    if data["target"] != scriptobj:
      break
    move_back_to_currency_tab()

def crafting(scriptobj, workitem: CraftingWorkItem, resetscript=True):
  queue = deque(workitem.positions)
  while len(queue) > 0:
    try_close_chat()
    current = queue.popleft()
    print(f"Placing item from inventory {current}")
    place_item(current)
    if data["target"] != scriptobj:
      break
    if pag.locateOnScreen(Images.showcase_empty, grayscale=True, confidence=0.8, region=REGION["showcase_box"]):
      print("Showcase empty, going to the next one...")
      continue
    pick_up_by_image(INACTIVE_CURRENCY_IMGS["alt"])
    moveto(LOCATIONS["showcase"])
    press('ctrl')
    press('altleft')
    press('shift')
    click()
    time.sleep(0.2)
    press_release('c', delay=0.2)
    press_release('c', delay=0.2)

    item = Item(pc.paste())
    try:
      item_config = BaseItemConfig.get_config_by_base_name(item)
    except Exception as e:
      print(f"Item parser failed: {e}")
      double_release(["ctrl", "shift", "altleft"])
      return_item()
      dump_tab_it()
      move_back_to_currency_tab()
      continue

    num_affixes_required = item_config.get("num_affixes_required")
    while not is_valid(item, item_config):
      # Scour and transmute if we have a rare item
      pick_up_alt = item.rarity == "Rare" or item.rarity == "Normal"
      if item.rarity == "Rare":
        scour_it()
        transmute_it()
      elif item.rarity == "Normal":
        transmute_it()

      if pick_up_alt:
        pick_up_by_image(INACTIVE_CURRENCY_IMGS["alt"])
        press('shift')
        moveto(LOCATIONS["showcase"], delay=0.06)

      click(delay=0)
      item = safe_copy_item(item)

      # Augment if we have less than 2 affixes and we have a good prefix or suffix
      augged = False
      if num_affixes_required >= 2 and len(item.affixes) < 2 and (good_prefixes(item, item_config) + good_suffixes(item, item_config) >= 1):
        augged = True
        aug_it()
        item = safe_copy_item(item)

      # Regal if we have less than 3 affixes and we have 2 good prefixes or suffixes
      if num_affixes_required >= 3 and len(item.affixes) < 3 and (good_prefixes(item, item_config) + good_suffixes(item, item_config) >= 2):
        regal_it()
        item = safe_copy_item(item)

      if augged:
        pick_up_by_image(INACTIVE_CURRENCY_IMGS["alt"])
        press('shift')
        moveto(LOCATIONS["showcase"], delay=0.06)
      if data["target"] != scriptobj:
        break

    double_release(["ctrl", "shift", "altleft"])
    try_close_chat()
    if data["target"] != scriptobj:
      break      
    else:
      play_audio()
    if data["target"] != scriptobj:
      break
    return_item()
    # Move it to the dump tab
    dump_tab_it()
    # Move back to currency tab
    move_back_to_currency_tab()


  if resetscript:
    data["target"] = None

def crafting_1x2(scriptobj):
  workitem = CraftingWorkItem(
    [(0,0), (2,0), (0,1), (2,1), (0,2), (2,2), (0,3), (2,3), (0,4), (2,4), (0,5), (2,5), (0,6), (2,6), (0,7), (2,7), (0,8), (2,8), (0,9), (2,9), (0,10), (2,10)]
  )
  crafting(scriptobj, workitem)

def crafting_2x4(scriptobj):
  workitem = CraftingWorkItem(
    [(0,0), (0,2), (0,4), (0,6), (0,8), (0,10)]
  )
  crafting(scriptobj, workitem)
  
def crafting_1x1(scriptobj):
  workitem = CraftingWorkItem(
    [(0,0), (1,0), (2,0), (3,0), (4,0)]
  )
  crafting(scriptobj, workitem)

def craft_until_highlight(scriptobj):
  def roll_until_highlight_or_empty(script_key, skipFirst=False):
    if pag.locateOnScreen(Images.showcase_empty, grayscale=True, confidence=0.8, region=REGION["showcase_box"]):
      print("Showcase empty, going to the next one...")
      return False
    pick_up_by_image(INACTIVE_CURRENCY_IMGS["alt"])
    press('shift')
    moveto(LOCATIONS["showcase"])
    while skipFirst or not highlight():
      click()
      time.sleep(0.1)
      skipFirst = False
      if data["target"] != script_key:
        return False
    release('shift')
    release('shift')
    return True

  global scripts
  queue = deque([(0,0)])
  if data["cmd"].get("highlight") == "bow":
    queue = deque([(0,0), (0,2), (0,4), (0,6), (0,8), (0,10)])

  while len(queue) > 0:
    current = queue.popleft()
    place_item(current)
    if roll_until_highlight_or_empty(scriptobj):
      play_audio()
    double_release(["ctrl", "shift"])
    if data["target"] != scriptobj:
      break
    return_item()
  data["target"] = None

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
  while pag.locateOnScreen(Images.chat_local_tab, grayscale=True, confidence=0.8):
    press('enter', 0.1)

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
  release('shift', delay=0.01)
  release('shift', delay=0.01)
  pick_up_by_image(INACTIVE_CURRENCY_IMGS[currency])
  moveto(LOCATIONS["showcase"], delay=0.06)
  click(delay=0.05)

def aug_it():
  use_it("aug")

def regal_it(): 
  use_it("regal")

def transmute_it():
  use_it("transmute")

def scour_it():
  use_it("scour")

def pick_up(name):
  release('shift')
  moveto(CURRENCY_LOCATIONS[name])
  right_click()
  
# I have more than 2 stacks of alts > 5000 quantity, they're in different coordinates
def pick_up_by_image(img):
  release('shift', delay=0.01)
  loc = pag.locateOnScreen(img, confidence=0.9, grayscale=True, region=REGION["stash"])
  if not loc:
    print(f"Image {img} not found, moving mouse away")
    moveto((randint(0, 115), randint(0, 2400)), delay=0.1)
  loc = pag.locateOnScreen(img, confidence=0.9, grayscale=True, region=REGION["stash"])
  if not loc:
    raise Exception(f"Image {img} not found on screen")
  moveto(loc, delay=0.05)
  right_click(delay=0.01)
  
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
  print(f"  {CRAFTING_1x2_KEY} - start/end 1x2 craft")
  print(f"  {CRATING_1x1_KEY} - start/end 2x4 craft")
  print(f"  {CRATING_1x1_KEY} - start/end 1x1 craft")
  # print(f"  {AUTO_POT_KEY} - start/end auto pot (press 2 when mana reaches 40%, press 1 when hp reaches 60%)")
  print(f"  {CRAFT_UNTIL_HIGHLIGHT_KEY} - start/end craft until highlight")
  print(f"  {CRAFT_FROM_QUEUE_TAB_KEY} - start/end craft from queue tab")
  print(f"  {PRESS_E_EVERY_INTERVAL_KEY} - start/end press E every interval (for auto vaal haste)")
  # print(f"  {CRAFT_INT_STACK_CLUSTER_KEY} - start/end craft int stack cluster [\"glo|gli|pow|pot|prod|teor\"]")
  print(f"  {CANCEL_KEY} - cancel all scripts")

if __name__=="__main__":
  main()
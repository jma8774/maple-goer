import pyautogui as pag
import keyboard
import time
import threading

# Images
class Images:
  CRAFT           = 'craft.png'
  OK_START        = 'ok_start.png'
  OK_END          = 'ok_end.png'
  CANCEL          = "cancel.png"
  HERBALISM       = "herbalism.png"
  EXTRACT_UP      = "extract_up.png"
  CONFIRM         = "confirm.png"
  HERB_BAG        = "herb_bag.png"
  SORT            = "sort.png"
  ENHANCE_STAR    = "enhance_star.png"
  ENHANCE_ENHANCE = "enhance_enhance.png"
  ENHANCE_OK      = "enhance_ok.png"
  CUBE_ONEMORETRY = "cube_onemoretry.png"

class Scripts:
  def __init__(self, obj):
    for (key, value) in obj.items():
      setattr(self, key, value)

# Hotkeys
CRAFT_WAP_KEY = 'ctrl+f1'
EXTRACT_KEY = 'ctrl+f2'
OPEN_HERB_BAGS_KEY = 'ctrl+f3'
ENHANCE_KEY = 'ctrl+f4'
CUBE_LEGENDARY_KEY = 'ctrl+f5'

# Data
data = {
  "target": None
}

def main():
  commands()
  scripts = Scripts({
    "WAP_CRAFT": craftWAP,
    "EXTRACT": extract,
    "OPEN_HERB_BAGS": openHerbBags,
    "ENHANCE": enhance,
    "CUBE_LEGENDARY": cube_to_legendary
  })
  keyboard.add_hotkey(CRAFT_WAP_KEY, lambda: toggleScript("WAP crafting", scripts.WAP_CRAFT))
  keyboard.add_hotkey(EXTRACT_KEY, lambda: toggleScript("equipment extraction", scripts.EXTRACT))
  keyboard.add_hotkey(OPEN_HERB_BAGS_KEY, lambda: toggleScript("open herb bags", scripts.OPEN_HERB_BAGS))
  keyboard.add_hotkey(ENHANCE_KEY, lambda: toggleScript("enhance gear", scripts.ENHANCE))
  keyboard.add_hotkey(CUBE_LEGENDARY_KEY, lambda: toggleScript("enhance gear", scripts.CUBE_LEGENDARY))
  while True:
    while data["target"] == None: 
      keyboard.read_key()
    thread = threading.Thread(target=lambda: data["target"](scripts))
    thread.start()
    thread.join()

def enhance(scripts):
  location = pag.locateOnScreen(Images.ENHANCE_ENHANCE, confidence=0.8)
  while True:
    pag.click(location)
    time.sleep(0.01)
    # clickIfFound(Images.ENHANCE_ENHANCE)
    # time.sleep(0.01)
    # moveToIfFound(Images.ENHANCE_STAR)
    # time.sleep(0.01)
    # clickIfFound(Images.ENHANCE_OK)
    # time.sleep(0.01)
    if data["target"] != scripts.ENHANCE:
      break
    
def cube_to_legendary(scripts):
  keyboard.press('enter')
  location = pag.locateOnScreen(Images.CUBE_ONEMORETRY, confidence=0.8)
  while True:
    pag.click(location)
    time.sleep(0.01)
    if data["target"] != scripts.ENHANCE:
      keyboard.release('enter')
      break
    
def openHerbBags(scripts):
  herbLocation = None
  okLocation = None
  sortLocation = None
  while True:
    if herbLocation is None:
      herbLocation = pag.locateOnScreen(Images.HERB_BAG, confidence=0.8)
    if okLocation is None:
      okLocation = pag.locateOnScreen(Images.OK_START, confidence=0.8)
    if sortLocation is None:
      sortLocation = pag.locateOnScreen(Images.SORT, confidence=0.8)
    pag.doubleClick(herbLocation)
    time.sleep(0.01)
    pag.click(okLocation)
    time.sleep(0.01)
    pag.moveTo(sortLocation)
    time.sleep(0.01)
    if data["target"] != scripts.OPEN_HERB_BAGS:
      break
    
def extract(scripts):
  while True:
    clickIfFound(Images.EXTRACT_UP)
    time.sleep(0.05)
    clickIfFound(Images.CONFIRM)
    time.sleep(0.05)
    clickIfFound(Images.OK_START)
    time.sleep(0.05)
    clickIfFound(Images.OK_END)
    time.sleep(0.05)
    if data["target"] != scripts.EXTRACT:
      break

def craftWAP(scripts):
  while True:
    time.sleep(0.05)
    clickIfFound(Images.CRAFT)
    time.sleep(0.05)
    clickIfFound(Images.OK_START)
    time.sleep(0.05)
    clickIfFound(Images.OK_END)
    time.sleep(0.05)
    # clickIfFound(Images.CANCEL)
    # time.sleep(0.05)
    moveToIfFound(Images.HERBALISM)
    if data["target"] != scripts.WAP_CRAFT:
      break
    time.sleep(30)
    if data["target"] != scripts.WAP_CRAFT:
      break

def toggleScript(msg, scriptId):
  if data["target"] is not None and data["target"] != scriptId:
    print("Stopping previously running script before starting...")
  data["target"] = None if data["target"] == scriptId else scriptId
  if data["target"] == scriptId:
    print(f"\nStart {msg}")
  else:
    print(f"Stop {msg}")

def moveToIfFound(image, confidence=0.8):
  executeIfFound(image, pag.moveTo, confidence=confidence)

def clickIfFound(image, confidence=0.8):
  executeIfFound(image, pag.click, confidence=confidence)

def doubleClickIfFound(image, confidence=0.8):
  executeIfFound(image, pag.doubleClick, confidence=confidence)

def executeIfFound(image, fn, confidence=0.8):
  location = pag.locateOnScreen(image, confidence=confidence)
  if location:
    fn(location)

def commands():
  print("Commands:")
  print(f"  {CRAFT_WAP_KEY} - start/end wap crafting")
  print(f"  {EXTRACT_KEY} - start/end extract equips")
  print(f"  {OPEN_HERB_BAGS_KEY} - start/end open herb bags")
  print(f"  {ENHANCE_KEY} - start/end gear enhancement")
  print(f"  {CUBE_LEGENDARY_KEY} - start/end cube to legendary")

main()
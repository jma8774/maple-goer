import pyautogui as pag
import keyboard
import time
import threading
from PIL import Image

def openImage(file):
  return Image.open(f"images/{file}")

# Images
class Images:
  CRAFT           = openImage('craft.png')
  OK_START        = openImage('ok_start.png')
  OK_END          = openImage('ok_end.png')
  CANCEL          = openImage("cancel.png")
  HERBALISM       = openImage("herbalism.png")
  EXTRACT_UP      = openImage("extract_up.png")
  CONFIRM         = openImage("confirm.png")
  HERB_BAG        = openImage("herb_bag.png")
  SORT            = openImage("sort.png")
  ENHANCE_STAR    = openImage("enhance_star.png")
  ENHANCE_ENHANCE = openImage("enhance_enhance.png")
  ENHANCE_OK      = openImage("enhance_ok.png")
  CUBE_ONEMORETRY = openImage("cube_onemoretry.png")
  ASCENDION       = openImage("ascendion.png")
  WHITESCREEN     = openImage("whitescreen.png")
  BLACKSCREEN     = openImage("blackscreen.png")
  ZAKUM           = openImage("zakum.png")
  MS_ICON         = openImage("ms_icon.png")
  LIMINIA_ICON    = openImage("liminia_icon.png")

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

def test(scripts):
  while True:
    location = pag.locateOnScreen(Images.ASCENDION, confidence=0.8)
    pag.moveTo(location)
    print(location)
    time.sleep(2)
    if data["target"] != scripts.ENHANCE:
      break
    

def enhance(scripts):
  location = pag.locateOnScreen(Images.ENHANCE_ENHANCE, confidence=0.8)
  while True:
    pag.click(location)
    time.sleep(0.01)
    if data["target"] != scripts.ENHANCE:
      break
    
def cube_to_legendary(scripts):
  keyboard.press('enter')
  location = pag.locateOnScreen(Images.CUBE_ONEMORETRY, confidence=0.8)
  while True:
    pag.click(location)
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

def moveToIfFound(image, confidence=0.8, grayscale=True):
  executeIfFound(image, pag.moveTo, confidence=confidence, grayscale=grayscale)

def clickIfFound(image, confidence=0.8, grayscale=True):
  executeIfFound(image, pag.click, confidence=confidence, grayscale=grayscale)

def doubleClickIfFound(image, confidence=0.8, grayscale=True):
  executeIfFound(image, pag.doubleClick, confidence=confidence, grayscale=grayscale)

def executeIfFound(image, fn, confidence=0.8, grayscale=True):
  location = pag.locateOnScreen(image, confidence=confidence, grayscale=grayscale)
  if location:
    fn(location)

def commands():
  print("Commands:")
  print(f"  {CRAFT_WAP_KEY} - start/end wap crafting")
  print(f"  {EXTRACT_KEY} - start/end extract equips")
  print(f"  {OPEN_HERB_BAGS_KEY} - start/end open herb bags")
  print(f"  {ENHANCE_KEY} - start/end gear enhancement")
  print(f"  {CUBE_LEGENDARY_KEY} - start/end cube to legendary")

if __name__=="__main__":
  main()
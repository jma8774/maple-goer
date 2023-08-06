import pyautogui as pag
import time
import threading
from images import Images

# Create own custom classes to simulate these classes... they use win32/user32 microsoft libraries which flags the events as LowLevelKeyHookInjected
import pyautogui as pag

# Interception library to simulate  events without flagging them as LowLevelKeyHookInjected
import interception
from listener import KeyListener

class Scripts:
  def __init__(self, obj):
    for (key, value) in obj.items():
      setattr(self, key, value)

# Hotkeys
CRAFT_WAP_KEY = 'f1'
EXTRACT_KEY = 'f2'
OPEN_HERB_BAGS_KEY = 'f3'
ENHANCE_KEY = 'f4'

# Data
stop_flag = [False]
data = {
  "target": None
}

def main():
  # Interception Setup for main loop
  kdevice = interception.listen_to_keyboard()
  mdevice = interception.listen_to_mouse()
  interception.inputs.keyboard = kdevice
  interception.inputs.mouse = mdevice

  # Interception Key Listener Setup (seperate thread)
  scripts = Scripts({
    "WAP_CRAFT": craftWAP,
    "EXTRACT": extract,
    "OPEN_HERB_BAGS": openHerbBags,
    "ENHANCE": enhance,
  })
  kl = KeyListener(stop_flag)
  kl.add(CRAFT_WAP_KEY, lambda: toggleScript("WAP crafting", scripts.WAP_CRAFT))
  kl.add(EXTRACT_KEY, lambda: toggleScript("equipment extraction", scripts.EXTRACT))
  kl.add(OPEN_HERB_BAGS_KEY, lambda: toggleScript("open herb bags", scripts.OPEN_HERB_BAGS))
  kl.add(ENHANCE_KEY, lambda: toggleScript("enhance gear", scripts.ENHANCE))
  kl.run()

  commands()
  try:
    while True:
      while data["target"] == None: 
        time.sleep(1)
        continue
      thread = threading.Thread(target=lambda: data["target"](scripts))
      thread.start()
      thread.join()
  except KeyboardInterrupt:
    print("Exiting...")
    stop_flag[0] = True

def enhance(scripts):
  location = pag.locateCenterOnScreen(Images.ENHANCE_ENHANCE, confidence=0.8)
  while True:
    click(location)
    time.sleep(0.01)
    if data["target"] != scripts.ENHANCE:
      break
    
def openHerbBags(scripts):
  herbLocation = None
  okLocation = None
  sortLocation = None
  while True:
    if herbLocation is None:
      herbLocation = pag.locateCenterOnScreen(Images.BAG, confidence=0.8)
    if okLocation is None:
      okLocation = pag.locateCenterOnScreen(Images.OK_START, confidence=0.8)
    if sortLocation is None:
      sortLocation = pag.locateCenterOnScreen(Images.SORT, confidence=0.8)
    doubleclick(herbLocation)
    time.sleep(0.02)
    click(okLocation)
    time.sleep(0.01)
    moveto(sortLocation)
    time.sleep(0.015)
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
    moveToIfFound(Images.TAB_RESET)
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

def click(location):
  interception.click(location)

def moveto(location):
  interception.move_to(location)

def doubleclick(location):
  interception.click(location)
  time.sleep(0.02)
  interception.click(location)

def moveToIfFound(image, confidence=0.8, grayscale=True):
  executeIfFound(image, moveto, confidence=confidence, grayscale=grayscale)

def clickIfFound(image, confidence=0.8, grayscale=True):
  executeIfFound(image, click, confidence=confidence, grayscale=grayscale)

def executeIfFound(image, fn, confidence=0.8, grayscale=True):
  location = pag.locateCenterOnScreen(image, confidence=confidence, grayscale=grayscale)
  if location:
    fn(location)

def commands():
  print("Commands:")
  print(f"  {CRAFT_WAP_KEY} - start/end wap crafting")
  print(f"  {EXTRACT_KEY} - start/end extract equips")
  print(f"  {OPEN_HERB_BAGS_KEY} - start/end open herb bags")
  print(f"  {ENHANCE_KEY} - start/end gear enhancement")

if __name__=="__main__":
  main()
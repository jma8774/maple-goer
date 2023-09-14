import pyautogui as pag
import time
import threading
from base import Images, Audio, KeyListener
import pyautogui as pag
import interception

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
data = {
  'stop_flag': False,
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
  kl = KeyListener(data)
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
    print("Exiting... (Try spamming CTRL + C)")
    data['stop_flag'] = True

def enhance(scripts):
  location = pag.locateCenterOnScreen(Images.ENHANCE_ENHANCE, confidence=0.8)
  while data["target"] == scripts.ENHANCE:
    click(location)
    time.sleep(0.01)
    
def openHerbBags(scripts):
  seq = 0
  while data["target"] == scripts.OPEN_HERB_BAGS:
    if seq % 10 == 0 and not pag.locateCenterOnScreen(Images.BAG, confidence=0.8):
      data["target"] = None
    press_release('f9')
    time.sleep(0.20)
    press_release('y')
    time.sleep(0.25)
    seq += 1
    print(seq)
    
def extract(scripts):
  while data["target"] == scripts.EXTRACT:
    clickIfFound(Images.EXTRACT_UP)
    time.sleep(0.05)
    clickIfFound(Images.CONFIRM)
    time.sleep(0.05)
    clickIfFound(Images.OK_START)
    time.sleep(0.05)
    clickIfFound(Images.OK_END)
    time.sleep(0.05)

def craftWAP(scripts):
  while data["target"] == scripts.WAP_CRAFT:
    time.sleep(0.1)
    clickIfFound(Images.CRAFT)
    time.sleep(0.3)
    clickIfFound(Images.OK_START)
    time.sleep(5)
    clickIfFound(Images.OK_END)
    time.sleep(0.1)
    moveToIfFound(Images.TAB_RESET)
    time.sleep(0.1)
    clickIfFound(Images.ALCHEMY_TAB)
    if data["target"] != scripts.WAP_CRAFT:
      break
    time.sleep(10)

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

def press(key, delay=0.05):
  interception.key_down(key)
  time.sleep(delay)
  
def release(key, delay=0.05):
  interception.key_up(key)
  time.sleep(delay)

def press_release(key, delay=0.05):
  press(key)
  release(key, delay)

def commands():
  print("Commands:")
  print(f"  {CRAFT_WAP_KEY} - start/end wap crafting")
  print(f"  {EXTRACT_KEY} - start/end extract equips")
  print(f"  {OPEN_HERB_BAGS_KEY} - start/end open herb bags")
  print(f"  {ENHANCE_KEY} - start/end gear enhancement")

if __name__=="__main__":
  main()
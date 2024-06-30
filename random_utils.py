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
LOGIN_CHARS_FOR_1HOUR_KEY = 'f5'
REFRESH_BOSS_KEY = 'f6'

# Data
data = {
  'stop_flag': False,
  "target": None
}

def main():
  interception.set_maplestory()
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
    "LOGIN_CHARS_FOR_1HOUR": loginChars1Hour,
    "REFRESH_BOSS": refreshboss
  })
  kl = KeyListener(data)
  kl.add(CRAFT_WAP_KEY, lambda: toggleScript("WAP crafting", scripts.WAP_CRAFT))
  kl.add(EXTRACT_KEY, lambda: toggleScript("equipment extraction", scripts.EXTRACT))
  kl.add(OPEN_HERB_BAGS_KEY, lambda: toggleScript("open herb bags", scripts.OPEN_HERB_BAGS))
  kl.add(ENHANCE_KEY, lambda: toggleScript("enhance gear", scripts.ENHANCE))
  kl.add(LOGIN_CHARS_FOR_1HOUR_KEY, lambda: toggleScript("login to each chars for 1 hour to reset guild skills", scripts.LOGIN_CHARS_FOR_1HOUR))
  kl.add(REFRESH_BOSS_KEY, lambda: toggleScript("refresh boss ui", scripts.REFRESH_BOSS))
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

def refreshboss(scripts):
  while data["target"] == scripts.REFRESH_BOSS:
    refresh_loc = pag.locateCenterOnScreen(Images.REFRESH_BOSS, confidence=0.9, grayscale=True)
    if refresh_loc:
      interception.click(refresh_loc)
      time.sleep(0.5)
      interception.move_to(refresh_loc.x, refresh_loc.y + 50)
    time.sleep(3)
    
def loginChars1Hour(scripts):
  while data["target"] == scripts.LOGIN_CHARS_FOR_1HOUR:
    # Start from the character already logged in
    # Wait 1 hour
    print("Waiting 1 hour...")
    time.sleep(3605)

    # time.sleep(60)

    # Log off
    print("Logging off...")
    while pag.locateOnScreen(Images.SETTING, confidence=0.8, grayscale=True) == None:
      press_release('escape')
      time.sleep(1)
    press_release('up', 0.5)
    press_release('enter', 0.5)
    press_release('enter', 0.5)
    press_release('enter', 0.5)
    time.sleep(10)

    # Go to next character
    print("Going to next character...")
    rebootLoc = pag.locateCenterOnScreen(Images.REBOOT, confidence=0.8, grayscale=True)
    while rebootLoc != None:
      interception.click(rebootLoc)
      time.sleep(1)
      press_release('enter')
      time.sleep(10)
      interception.move_to((25, 25))
      rebootLoc = pag.locateCenterOnScreen(Images.REBOOT, confidence=0.8, grayscale=True)

    # Enter the character   
    print("Entering character...")
    press_release('right')
    time.sleep(1)
    press_release('enter')
    
def enhance(scripts):
  location = pag.locateCenterOnScreen(Images.ENHANCE_ENHANCE, confidence=0.8)
  while data["target"] == scripts.ENHANCE:
    click(location)
    time.sleep(0.005)
    
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
    interception.click()
    time.sleep(1)
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
  print(f"  {LOGIN_CHARS_FOR_1HOUR_KEY} - start/end login to each chars for 1 hour to reset guild skills (start from the character you want already logged in)")
  print(f"  {REFRESH_BOSS_KEY} - start/end refresh boss ui")

if __name__=="__main__":
  main()
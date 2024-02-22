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
AUTO_LOSE_KEY = 'f1'

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
    "AUTO_LOSE": autoLose,
  })
  kl = KeyListener(data)
  kl.add(AUTO_LOSE_KEY, lambda: toggleScript("auto lose", scripts.AUTO_LOSE))
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

def autoLose(scripts):
  while data["target"] == scripts.AUTO_LOSE:
    interception.move_to((20, 20))
    time.sleep(1)
    clickIfFound(Images.CR_BATTLE)
    time.sleep(1)
    clickIfFound(Images.CR_OK)
    time.sleep(1)
    if data["target"] != scripts.AUTO_LOSE:
      break
    time.sleep(5)

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
  print(f"  {AUTO_LOSE_KEY} - start/end auto lose")

if __name__=="__main__":
  main()
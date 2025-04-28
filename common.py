import random
from state import state
from pyautogui import locateOnScreen, locateCenterOnScreen, locateAllOnScreen
import time

minimap_rune_region = (0, 0, 500, 300)

def pause_if_whiteroom(pag, data, map):
  minimap_map_icon_region = (0, 0, 55, 55)
  if state['fakefullscreen']:
    minimap_map_icon_region = (0, 0, 60, 100)
  if not pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True):
    print("Double checking minimap region")
    if pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def print_state(state: dict):
  print("States")
  for key, value in state.items():
    print('  {:<12}  {:<12}'.format(key+":", value))

def print_args(args):
  print("Arguments")
  for arg in args:
    print(f"  {arg}")

def print_scripts(scripts: dict):
  print("Scripts")
  for key, value in scripts.items():
    print('  {:<12}  {:<12}'.format(key+":", str(value)))

def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

def locate_on_screen(image, region=None, confidence=1, grayscale=False, **kwargs):
  if region is None and state['fakefullscreen']:
    region = (0, 0, 1366, 768)
  return locateOnScreen(image, region=region, confidence=confidence, grayscale=grayscale, **kwargs)


def locate_center_on_screen(image, region=None, confidence=1, grayscale=False, **kwargs):
  if region is None and state['fakefullscreen']:
    region = (0, 0, 1366, 768)
  return locateCenterOnScreen(image, region=region, confidence=confidence, grayscale=grayscale, **kwargs)

def locate_all_on_screen(image, region=None, confidence=1, grayscale=False, **kwargs):
  if region is None and state['fakefullscreen']:
    region = (0, 0, 1366, 768)
  return locateAllOnScreen(image, region=region, confidence=confidence, grayscale=grayscale, **kwargs)

def sleep(seconds, randomize_percentage=0.03):
  time.sleep(seconds + random.uniform(randomize_percentage * -seconds, randomize_percentage * seconds))

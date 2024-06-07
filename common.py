import random

def pause_if_whiteroom(pag, data, map):
  minimap_map_icon_region = (0, 0, 55, 55)
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
import time
import random
import sys
from datetime import datetime, timedelta
from base import BotBase, Images
import pyautogui as pag
from state import state

vj_mob_region = (0, 200, 450, 500)
minimap_map_icon_region = (0, 0, 55, 55)
def getMap():
  maps = {
    "vj": Images.VANISHING_ICON,
    "chuchu": Images.CHUCHU_ICON,
    "lach": Images.LACH_ICON,
    "default": Images.VANISHING_ICON
  }
  return maps[state['script']] if state['script'] in maps else maps['default']

b = None
data = {
  'next_buff': datetime.now(),
  'next_infinity': datetime.now(),
  'next_infinity2': datetime.now(),

  'next_creeping': datetime.now(),
  'next_web': datetime.now(),
  'next_poison_nova': datetime.now(),
  'next_dot': datetime.now(),
  'next_poison_chain': datetime.now(),
  'next_meteor': datetime.now(),
  'next_elemental': datetime.now(),
  'next_megiddo': datetime.now(),
  'next_erda_fountain': datetime.now(),

  'next_loot_2': datetime.now() + timedelta(minutes=1.5),
}

def main():
  global b

  scripts = {
    "vj": vj_macro,
    "chuchu": chuchu_macro,
    "lach": lach_macro,
    "default": vj_macro,
  }

  for arg in sys.argv:
    if arg == 'nomap':
      state['checkmap'] = False
    elif arg == 'nomobscan':
      state['scanmob'] = False
    elif arg == 'nostatus':
      state['sendstatus'] = False
    elif arg == 'norune':
      state['checkrune'] = False
    elif arg == 'dev':
      state['checkmap'] = False
      state['scanmob'] = False
      state['sendstatus'] = False
    elif arg in scripts:
      state['script'] = arg
    state['localserver'] = True
    
  b = BotBase(data, {
    "user": "jeemong",
    "script": scripts[state['script']],
    "setup": setup
  })
  print(state)
  b.run()
    
def setup():
  pass

def lach_macro():
  print("Started Victory Plate Street 1 macro")
  while not should_pause():
    buff_setup()
    if not poison_nova():
      if not dot():
        if not poison_chain():
          if not meteor():
            if not elemental():
              if not megiddo():
                pass
              
    if should_pause(): return
    teleport_dir('down')
    if should_pause(): return
    creeping_toxic()
    if should_pause(): return
    q()
    if should_pause(): return
    teleport_dir('up', 0.5)
    time.sleep(7)
  print("Paused Victory Plate Street 1 macro")

def chuchu_macro():
  print("Started Slurpy Forest Depths macro")
  while not should_pause():
    buff_setup()
    if not poison_nova():
      if not dot():
        if not poison_chain():
          if not meteor():
            if not elemental():
              if not megiddo():
                pass
              
    if should_pause(): return
    teleport_dir('down')
    if should_pause(): return
    creeping_toxic()
    if should_pause(): return
    q()
    if should_pause(): return
    teleport_dir('up', 0.5)
    time.sleep(7)
  print("Paused Slurpy Forest Depths macro")

def vj_macro():
  print("Started Rock Zone macro")
  while not should_pause():
    buff_setup()
    if not poison_nova():
      if not dot():
        if not poison_chain():
          if not meteor():
            if not elemental():
              if not megiddo():
                pass
              
    if should_pause(): return
    teleport_dir('down')
    if should_pause(): return
    creeping_toxic()
    if should_pause(): return
    q()
    if should_pause(): return
    teleport_dir('up', 0.5)
    # if datetime.now() > data['next_erda_fountain']:
    #   if should_pause(): return
    #   teleport_dir('left')
    #   if should_pause(): return
    #   teleport_dir('left')
    #   if should_pause(): return
    #   teleport_dir('up')
    #   if should_pause(): return
    #   erda_fountain()
    #   if should_pause(): return
    #   teleport_dir('down')
    #   if should_pause(): return
    #   teleport_dir('right')
    #   if should_pause(): return
    #   teleport_dir('right')
    # else:
    time.sleep(7)
  print("Paused Rock Zone macro")

def buff_setup():
  cur = datetime.now()
  
  b.check_person_entered_map(only_guild=True)

  b.check_fam_leveling()
  
  b.check_tof("y")

  b.check_wap()

  b.check_fam_fuel()

  b.check_elite_box()

  b.check_rune(play_sound=False)

  if cur > data['next_buff']:
    b.press_release("pagedown", 1.5)
    data['next_buff'] = cur + timedelta(seconds=260)
  
  if cur > data['next_infinity']:
    b.press_release("delete", 1)
    data['next_infinity'] = cur + timedelta(seconds=180)
    data['next_infinity2'] = cur + timedelta(seconds=96)

  if cur > data['next_infinity2']:
    b.press_release("end", 1)
    data['next_infinity2'] = cur + timedelta(seconds=999)

def erda_fountain():
  if datetime.now() > data['next_erda_fountain']:
    b.press('down')
    b.press_release('b')
    b.press_release('b')
    b.release('down', delay=0.6)
    data['next_erda_fountain'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def creeping_toxic(delayAfter=0.7):
  if datetime.now() > data['next_creeping']:
    b.press_release('z', delayAfter)
    data['next_creeping'] = datetime.now() + timedelta(seconds=59)
    return True
  return False

def poison_nova(delayAfter=0.5):
  if datetime.now() > data['next_poison_nova']:
    b.press_release('s', delay=delayAfter)
    data['next_poison_nova'] = datetime.now() + timedelta(seconds=22)
    return True
  return False

def dot(delayAfter=0.9):
  if datetime.now() > data['next_dot']:
    b.press_release('d', delay=delayAfter)
    data['next_dot'] = datetime.now() + timedelta(seconds=22)
    return True
  return False

def poison_chain(delayAfter=0.7):
  if datetime.now() > data['next_poison_chain']:
    b.press_release('a', delay=delayAfter)
    data['next_poison_chain'] = datetime.now() + timedelta(seconds=22)
    return True
  return False

def meteor(delayAfter=0.7):
  if datetime.now() > data['next_meteor']:
    b.press_release('c', delay=delayAfter)
    data['next_meteor'] = datetime.now() + timedelta(seconds=44)
    return True
  return False

def megiddo(delayAfter=0.7):
  if datetime.now() > data['next_megiddo']:
    b.press_release('x', delay=delayAfter)
    data['next_megiddo'] = datetime.now() + timedelta(seconds=48)
    return True
  return False

def elemental(delayAfter=0.7):
  if datetime.now() > data['next_elemental']:
    b.press_release('2', delay=delayAfter)
    data['next_elemental'] = datetime.now() + timedelta(seconds=75)
    return True
  return False

def web(delayAfter=0.3):
  if datetime.now() > data['next_web']:
    b.press_release('4', delay=delayAfter)
    data['next_web'] = datetime.now() + timedelta(seconds=251)
    return True
  return False

def teleport(delay=0.6):
  b.press_release('shift', delay)

def teleport_dir(dir, delay=0.6):
  keycode = None
  if dir == 'left':
    keycode = 'left'
  elif dir == 'right':
    keycode = 'right'
  elif dir == 'up':
    keycode = 'up'
  elif dir == 'down':
    keycode = 'down'
  b.press(keycode)
  b.press_release('shift')
  b.release(keycode, delay=delay)

def q(delay=0.05):
  b.press_release('q', delay)

def should_pause():
  # If we confirmed that we are not in the same map but we are not paused yet, skip this so we don't check for images again
  if state['checkmap'] and not data['whiteroomed'] and pause_if_change_map(getMap()):
    data['whiteroomed'] = True
  return data['is_paused']

def pause_if_change_map(map):
  isSeeMap = pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True)
  if not isSeeMap:
    # Double check
    print("Double checking minimap region")
    if pag.locateOnScreen(map, confidence=0.5, region=minimap_map_icon_region, grayscale=True):
      return False
    data['is_paused'] = True
    return True
  return False

def uniform(a, b):
  rng = random.random()
  return a + rng*(b-a)

if __name__=="__main__":
  main()
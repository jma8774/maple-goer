from PIL import Image
import random
import threading
import interception
from interception._keycodes import KEYBOARD_MAPPING
import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import time
import pyautogui as pag
import pygame
import sys
from state import state
import pyscreeze
import common

pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = False

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

#region BOTBASE
TOF_KEY = 'f1'
WAP_KEY = 'f2'
AUTO_LEVEL_FAM_KEY = 'f3'
FAM_FUEL_KEY = 'f4'
START_KEY = 'f7'
PAUSE_KEY = 'f8'
NEXT_SCRIPT_KEY = 'f9'
minimap_rune_region = (0, 0, 500, 300)
buffs_region = (250, 0, 1366-250, 80)

def shutdown_computer():
    if os.name == 'nt':
        # For Windows operating system
        os.system('shutdown /s /t 0')
    elif os.name == 'posix':
        # For Unix/Linux/Mac operating systems
        os.system('sudo shutdown now')
    else:
        print('Unsupported operating system.')
        
class BotBase:
  def __init__(self, data, config, args=None, scripts=None):
    self.args = args
    self.scripts = scripts if scripts else {}
    self.setup_args()

    self.data = data
    self.config = config
    self.thread = None

    self.setup_data()
    self.setup_audio()

    # Interception Setup for main loop
    interception.set_maplestory()
    kdevice = interception.listen_to_keyboard()
    mdevice = interception.listen_to_mouse()
    interception.inputs.keyboard = kdevice
    interception.inputs.mouse = mdevice
    clear()

    # Interception Key Listener Setup (seperate thread)
    kl = KeyListener(data)
    if self.config['disable_extras'] != True:
      kl.add(TOF_KEY, self.handle_tof)
      kl.add(WAP_KEY, self.handle_wap)
      # kl.add(AUTO_LEVEL_FAM_KEY, self.handle_auto_level_fam)
      # kl.add(FAM_FUEL_KEY, self.handle_fam_fuel)
    kl.add(START_KEY, self.start)
    kl.add(PAUSE_KEY, self.pause)
    kl.add(NEXT_SCRIPT_KEY, self.next_script)
    kl.run()

    self.commands()

  def setup_args(self):
    if not self.args:
      return
    for arg in self.args:
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
      elif arg in self.scripts:
        state['script'] = arg
      state['localserver'] = True

  def setup_data(self):
    self.data['use_inventory_region'] = None

    self.data['tof_state'] = None
    self.data['tof_done'] = False
    self.data['next_tof_check'] = datetime.now()

    self.data['auto_level_fam_state'] = None
    self.data['auto_level_done'] = False
    self.data['next_level_fam_check'] = datetime.now()

    self.data['wap_state'] = False
    self.data['next_wap_check'] = datetime.now()

    self.data['fam_fuel_state'] = False
    self.data['next_fam_fuel_check'] = datetime.now()

    self.data['stop_flag'] = False
    self.data['is_paused'] = True
    self.data['time_started'] = None

    self.data['next_loot'] = datetime.now() + timedelta(minutes=1.7)
    self.data['key_pressed'] = {}
    self.data['whiteroomed'] = False
    self.data['next_rune_check'] = datetime.now()
    self.data['next_elite_box_check'] = datetime.now()
    self.data['someone_on_map_cooldown'] = datetime.now()

    self.config['disable_extras'] = self.config['disable_extras'] if 'disable_extras' in self.config else False

  def run(self):
    if "script" not in self.config:
      raise Exception("Config must have script functions")
    setup = self.config['setup'] if 'setup' in self.config else None
    
    try:
      while True:
        def scriptwrapper():
          script = self.scripts[state['script']] if self.scripts and self.scripts[state['script']] else self.config['script']
          try:
            script()
          except Exception as e:
            if str(e) != "Stopping thread":
              print(e)

        if self.data['is_paused'] == True:
          time.sleep(1)
          continue
        
        if self.data['time_started'] == None:
          post_status("started", { "user": self.config['user'] })
          self.data['time_started'] = datetime.now()

        # Setup for each new run
        if setup:
          setup()
        self.thread = threading.Thread(target=scriptwrapper)
        self.thread.start()
        self.thread.join()
        self.release_all()

        # Play sound if whiteroomed
        if self.data['whiteroomed']:
          print(f"Map change detected, script paused, playing audio: Press {PAUSE_KEY} to stop")
          post_status("whiteroom", { "user": self.config['user'] })
          self.play_audio(Audio.TYLER1_AUTISM)
    except KeyboardInterrupt:
      self.data['stop_flag'] = True
      self.post_summary_helper()
      print("Exiting... (Try spamming CTRL + C)")
  

  def check_fam_leveling(self, fam_menu_key='f11', summon_fam_key='f12'):
    if self.data['auto_level_done'] or self.data['auto_level_fam_state'] == None or datetime.now() < self.data['next_level_fam_check']:
      return
    mob = self.data['auto_level_fam_state']
    
    # Deselect current familiars
    if self.data['is_paused']: return
    self.press_release(fam_menu_key)
    time.sleep(0.5)
    setuploc = pag.locateCenterOnScreen(Images.SETUP, confidence=0.8, grayscale=True)
    interception.click(setuploc)
    time.sleep(0.5)
    interception.move_to(setuploc.x, setuploc.y + 150)
    time.sleep(0.2)
    if not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True):
      self.data['next_level_fam_check'] = datetime.now() + timedelta(minutes=10)
      post_fam_level({ "user": self.config['user'], "status": "NotLeveledYet"})
      self.press_release("escape")
      return
    interception.click(setuploc.x, setuploc.y + 150)
    interception.click(setuploc.x, setuploc.y + 150)
    time.sleep(0.1)
    interception.click(setuploc.x, setuploc.y + 150)
    interception.click(setuploc.x, setuploc.y + 150)
    time.sleep(0.1)
    interception.click(setuploc.x, setuploc.y + 150)
    interception.click(setuploc.x, setuploc.y + 150)
    time.sleep(0.1)
    interception.click(setuploc.x, setuploc.y + 150)
    interception.click(setuploc.x, setuploc.y + 150)

    # Find up to 2 familiars to train 
    if self.data['is_paused']: return
    time.sleep(0.1)
    fams = []
    if mob == 'ascendion':
      fams.extend(list(pag.locateAllOnScreen(Images.FAM_ASCENDION, confidence=0.8, grayscale=True)))
    elif mob == 'ascendion/foreberion':
      fams.extend(list(pag.locateAllOnScreen(Images.FAM_ASCENDION, confidence=0.8, grayscale=True)))
      fams.extend(list(pag.locateAllOnScreen(Images.FAM_FOREBERION, confidence=0.8, grayscale=True)))
    picked = 0
    for fam in fams:
      fam_pos = (fam.left + fam.width / 2, fam.top + fam.height / 2)
      interception.move_to(fam_pos)
      time.sleep(0.3)
      if not pag.locateOnScreen(Images.FAM_LEVEL5, confidence=0.9, grayscale=True):
        time.sleep(0.3)
        interception.click(fam_pos)
        interception.click(fam_pos)
        time.sleep(0.4)
        picked += 1
        if picked == 3:
          break
    if self.data['is_paused']: return
    if picked == 0:
      self.data['auto_level_done'] = True
      post_fam_level({ "user": self.config['user'], "status": "Done"})
    else:
      self.data['next_level_fam_check'] = datetime.now() + timedelta(minutes=30.5)
      post_fam_level({ "user": self.config['user'], "status": "Success"})
    time.sleep(0.4)
    ok_loc = pag.locateCenterOnScreen(Images.OK_START, confidence=0.8, grayscale=True) or pag.locateCenterOnScreen(Images.OK_END, confidence=0.8, grayscale=True)
    interception.click(ok_loc)
    time.sleep(0.8)

    # Save
    if self.data['is_paused']: return
    interception.move_to(setuploc)
    time.sleep(0.5)
    saveloc = pag.locateCenterOnScreen(Images.SAVE1366, confidence=0.8, grayscale=True)
    interception.click(saveloc)
    interception.click(saveloc)
    time.sleep(0.5)
    self.press_release("enter")
    time.sleep(0.5)
    self.press_release("escape")

    time.sleep(0.3)
    while not pag.locateOnScreen(Images.FAM_BUFF, confidence=0.9):
      self.press_release(summon_fam_key)
      time.sleep(0.5)
  
  def check_tof(self, npc_chat_key):
    if self.data['tof_done'] or self.data['tof_state'] == None or datetime.now() < self.data['next_tof_check']:
      return
    d = {
      "takeno": Images.TAKENO,
      "ibaraki": Images.IBARAKI
    }
    bulb_loc = pag.locateCenterOnScreen(Images.WHITE_QUEST_BULB)
    if not bulb_loc:
      print("Can't find white quest lightbulb")
      post_tof({ "user": self.config['user'], "status": "NoBulb"})
      self.data['next_tof_check'] = datetime.now() + timedelta(seconds=5)
      return
    interception.click(bulb_loc)
    time.sleep(0.5)
    if self.data['is_paused']: return
    
    # Complete quest
    quest_to_complete = pag.locateOnScreen(Images.TOF_COMPLETE, confidence=0.9, grayscale=True)
    if quest_to_complete:
      interception.click(quest_to_complete)
      time.sleep(2)
      while pag.locateOnScreen(Images.YES, confidence=0.6):
        self.press_release(npc_chat_key, delay=0.15)
        self.press_release(npc_chat_key, delay=0.15)
        self.press_release(npc_chat_key, delay=0.15)
        self.press_release(npc_chat_key, delay=0.15)
        self.press_release(npc_chat_key, delay=0.15)
        self.press_release(npc_chat_key, delay=0.15)
        time.sleep(0.2)

      # Check if it was completed
      interception.click(bulb_loc)
      time.sleep(0.5)
      if pag.locateOnScreen(Images.TOF_COMPLETE, confidence=0.6, grayscale=True):
        post_tof({ "user": self.config['user'], "status": "InProgress"})
        self.data['next_tof_check'] = datetime.now() + timedelta(minutes=5)
        self.press_release("escape")
        return
    
    # Open the board
    if self.data['is_paused']: return
    my_level_range_loc = pag.locateCenterOnScreen(Images.MY_LEVEL_RANGE, confidence=0.9, grayscale=True)
    if my_level_range_loc:
      interception.click(my_level_range_loc)
    time.sleep(0.3)
    board_quest = pag.locateCenterOnScreen(Images.TOF_BOARD, confidence=0.9, grayscale=True)
    interception.click(board_quest)
    time.sleep(0.5)

    # Click on the person
    if self.data['is_paused']: return
    person_loc = pag.locateOnScreen(d[self.data['tof_state']], confidence=0.9, grayscale=True)
    if not person_loc:
      print("Can't find person")
      post_tof({ "user": self.config['user'], "status": "NoPerson"})
      self.data['next_tof_check'] = datetime.now() + timedelta(seconds=5)
      return
    interception.click(person_loc)
    time.sleep(0.5)

    # Click on the ask button
    if self.data['is_paused']: return
    askLoc = pag.locateCenterOnScreen(Images.ASK, confidence=0.9, grayscale=True)
    if not askLoc:
      print("Can't find ASK")
      post_tof({ "user": self.config['user'], "status": "NoAsk"})
      self.data['next_tof_check'] = datetime.now() + timedelta(seconds=5)
      return
    time.sleep(0.5)
    interception.click(askLoc)
    interception.click(askLoc)
    interception.click(askLoc)
    time.sleep(1.5)

    # Check if next exist, if it exist, then we continue
    if self.data['is_paused']: return
    if not pag.locateOnScreen(Images.NEXT, confidence=0.60):
      print("Can't find NEXT, we are done?")
      post_tof({ "user": self.config['user'], "status": "Done"})
      self.data['tof_done'] = True
      self.press_release("escape")
      return

    # Accept the quest
    if self.data['is_paused']: return
    time.sleep(0.5)
    while pag.locateOnScreen(Images.NEXT, confidence=0.60):
      self.press_release(npc_chat_key, delay=0.15)
      self.press_release(npc_chat_key, delay=0.15)
      self.press_release(npc_chat_key, delay=0.15)
      self.press_release(npc_chat_key, delay=0.15)
      self.press_release(npc_chat_key, delay=0.15)
      self.press_release(npc_chat_key, delay=0.15)
      time.sleep(0.2)
    print("Started a new ask")
    post_tof({ "user": self.config['user'], "status": "Success"})
    self.data['next_tof_check'] = datetime.now() + timedelta(minutes=30.5)

    self.press_release("escape")

  def check_wap(self):
    dirty = False
    if not self.data['wap_state'] or datetime.now() < self.data['next_wap_check']:
      return
    
    if not self.update_use_inventory_region():
      print("Could not find inventory USE region to use wap")
      post_wap({ "user": self.config['user'], "status": "InventoryNotFound"})
      dirty = True

    expired = not pag.locateOnScreen(Images.WAP_BUFF, confidence=0.95, region=buffs_region)
    print("Wap expired: ", expired)
    if self.data['use_inventory_region'] and expired:
      interception.move_to(pag.locateCenterOnScreen(Images.CASH_TAB, confidence=0.9, grayscale=True) or (0, 0))
      wap_loc = pag.locateCenterOnScreen(Images.WAP, confidence=0.85, grayscale=True, region=self.data['use_inventory_region'])
      if self.data['is_paused']: return
      if wap_loc:
        time.sleep(0.2)
        interception.click(wap_loc)
        interception.click(wap_loc)
        time.sleep(0.7)
        cancel_loc = pag.locateCenterOnScreen(Images.CANCEL, confidence=0.9, grayscale=True)
        wapAlreadyActive = cancel_loc is not None
        if wapAlreadyActive:
          while cancel_loc:
            interception.click(cancel_loc)
            interception.move_to(pag.locateCenterOnScreen(Images.CASH_TAB, confidence=0.9, grayscale=True) or (0, 0))
            cancel_loc = pag.locateCenterOnScreen(Images.CANCEL, confidence=0.9, grayscale=True)
          post_wap({ "user": self.config['user'], "status": "AlreadyWapped"})
        else:
          success = pag.locateOnScreen(Images.WAP_BUFF, confidence=0.95, region=buffs_region)
          post_wap({ "user": self.config['user'], "status": "Success" if success else "Failed"})
        time.sleep(0.2)
      else:
        dirty = True

    if self.data['is_paused']: return
    if dirty:
      self.update_use_inventory_region(dirty)

    self.data['next_wap_check'] = datetime.now() + timedelta(minutes=1)

  def check_fam_fuel(self):
    dirty = False
    if not self.data['fam_fuel_state'] or datetime.now() < self.data['next_fam_fuel_check']:
      return
    
    if self.data['is_paused']: return
    if not self.update_use_inventory_region():
      print("Could not find inventory USE region to use familiar fuel")
      post_fam_fuel({ "user": self.config['user'], "status": "InventoryNotFound"})
      dirty = True

    if self.data['is_paused']: return
    expired = not pag.locateOnScreen(Images.FAM_BUFF, confidence=0.95, region=buffs_region)
    if not expired:
      print("Buff is not about to expire")
      # post_fam_fuel({ "user": self.config['user'], "status": "NotExpired"})
    if self.data['use_inventory_region'] and expired:
      interception.move_to(pag.locateCenterOnScreen(Images.CASH_TAB, confidence=0.9, grayscale=True) or (0, 0))
      fuel_loc = pag.locateCenterOnScreen(Images.FAM_FUEL, confidence=0.80, grayscale=True, region=self.data['use_inventory_region'])
      if fuel_loc:
        time.sleep(0.2)
        interception.click(fuel_loc)
        interception.click(fuel_loc)
        time.sleep(0.7)
        success = pag.locateOnScreen(Images.FAM_BUFF, confidence=0.95, region=buffs_region)
        post_fam_fuel({ "user": self.config['user'], "status": "Success" if success else "Failed"})
      else:
        post_fam_fuel({ "user": self.config['user'], "status": "CantFindFuel"})
        dirty = True
        
    if self.data['is_paused']: return
    if dirty:
      self.update_use_inventory_region(dirty)

    self.data['next_fam_fuel_check'] = datetime.now() + timedelta(seconds=30)

  def check_rune(self, play_sound=True, post_request=True):
    if datetime.now() > self.data['next_rune_check'] and state['checkrune']:
      if pag.locateOnScreen(Images.RUNE_MINIMAP, confidence=0.7, region=minimap_rune_region):
        if play_sound:
          self.play_audio(Audio.PING, loops=2)
        if post_request:
          post_status("rune", { "user": self.config['user'] })
      self.data['next_rune_check'] = datetime.now() + timedelta(seconds=60)

  def check_person_entered_map(self, only_guild=False):
    normal = None if only_guild else pag.locateOnScreen(Images.PERSON, region=minimap_rune_region)
    guild = pag.locateOnScreen(Images.GUILD_PERSON, region=minimap_rune_region)
    if normal or guild:
      cur = datetime.now()
      if cur >= self.data['someone_on_map_cooldown']:
        # post_status("someone_entered_map", { "user": self.config['user'] })
        if guild:
          post_status("guild_entered_map", { "user": self.config['user'] })
        self.play_audio(Audio.PING, loops=2 if guild else 1)
        self.data['someone_on_map_cooldown'] = cur + timedelta(seconds=5)

  def check_elite_box(self, boxkey='f6'):
    cur = datetime.now()
    if cur > self.data['next_elite_box_check']:
      boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
      while boxloc != None:
        self.press_release(boxkey)
        boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
      self.data['next_elite_box_check'] = cur + timedelta(seconds=45)

  def update_use_inventory_region(self, dirty=False):
    res = pag.size()
    if dirty or self.data['use_inventory_region'] is None:
      self.data['use_inventory_region'] = None
      equip_tab = pag.locateOnScreen(Images.FAM_EQUIP, confidence=0.9, grayscale=True)
      if equip_tab is not None:
        self.data['use_inventory_region'] = (equip_tab.left, equip_tab.top, min(675, res[0] - equip_tab.left), min(390, res[1] - equip_tab.top))
    return self.data['use_inventory_region'] is not None
  
  def post_summary_helper(self):
    if self.data['time_started'] != None:
      post_summary(self.data['time_started'], self.config['user'])
      self.data['time_started'] = None
    
  def pause(self):
    print('Pausing...')
    self.data['is_paused'] = True
    self.pause_audio()
    if self.thread:
      self.thread.join()
    print('Paused')

  def start(self):
    self.commands(True)
    print('\nStarting...')
    self.data['is_paused'] = False
    self.data['whiteroomed'] = False

  def next_script(self):
    keys = list(self.scripts.keys())
    current = state['script']
    index = keys.index(current)
    state['script'] = keys[(index + 1) % len(keys)]
    self.commands(True)
    print()
    print(f"Script changed from {current} -> {state['script']}")

  def handle_tof(self):
    if self.data['tof_state'] == None:
      self.data['tof_state'] = "takeno"
    elif self.data['tof_state'] == "takeno":
      self.data['tof_state'] = "ibaraki"
    elif self.data['tof_state'] == "ibaraki":
      self.data['tof_state'] = None
    self.commands(True)

  def handle_auto_level_fam(self):
    if self.data['auto_level_fam_state'] == None:
      self.data['auto_level_fam_state'] = "ascendion"
    elif self.data['auto_level_fam_state'] == "ascendion":
      self.data['auto_level_fam_state'] = "ascendion/foreberion"
    else:
      self.data['auto_level_fam_state'] = None
    self.commands(True)

  def handle_wap(self):
    self.data['wap_state'] = not self.data['wap_state']
    self.commands(True)

  def handle_fam_fuel(self):
    self.data['fam_fuel_state'] = not self.data['fam_fuel_state']
    self.commands(True)

  def setup_audio(self, volume=1):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)

  def play_audio(self, audio_file_path, loops=-1):
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play(loops=loops)

  def pause_audio(self):
    pygame.mixer.music.pause()

  def release_all(self):
    for key in self.data['key_pressed']:
      self.release(key)

  def press(self, key, delay=0.05):
    interception.key_down(key)
    self.data['key_pressed'][key] = True
    if delay > 0:
      time.sleep(delay)
    
  def release(self, key, delay=0.05):
    interception.key_up(key)
    self.data['key_pressed'][key] = False
    if delay > 0:
      time.sleep(delay)

  def press_release(self, key, delay=0.05, delayInBetween=0.05):
    self.press(key, delayInBetween)
    self.release(key, delay)

  def handle_next_config(self):
    if "next_config" in self.config:
      self.data['stop_flag'] = True
      self.config["next_config"]()
      self.commands(True)
  
  def commands(self, clearBefore=False):
    if clearBefore:
      clear()
    print(f"Make sure Maplestory is in 1366x768 resolution full screen mode")
    print()

    print("Commands:")
    if self.config['disable_extras'] != True:
      print(f"  {TOF_KEY} - auto thread of fate: [{self.data['tof_state'] if self.data['tof_state'] else 'disabled'}]")
      print(f"  {WAP_KEY} - auto wap: [{'enabled' if self.data['wap_state'] else 'disabled'}]")
      # print(f"  {AUTO_LEVEL_FAM_KEY} - auto level familiars: [{self.data['auto_level_fam_state'] if self.data['auto_level_fam_state'] else 'disabled'}]")
      # print(f"  {FAM_FUEL_KEY} - auto familiar fuel: [{'enabled' if self.data['fam_fuel_state'] else 'disabled'}]")
      print()
    print(f"  {START_KEY} - start")
    print(f"  {PAUSE_KEY} - pause")
    print(f"  {NEXT_SCRIPT_KEY} - next script")
    print()

    common.print_state(state)
    print()

    common.print_args(self.args)
    print()
    
    common.print_scripts(self.scripts)
    print()

    print("If you want to run the script and not use any image detection (allowing you to run the script in ANY resolution) add 'dev' as an argument when running the script.")
    print("  For example, `python <name of python file> dev` or `python steven.py dev`") 
#endregion BOT

#region ASSESTS
def openImage(file):
  return Image.open(f"images/{file}")

# Images
class Images:
  CRAFT             = openImage('craft.png')
  OK_START          = openImage('ok_start.png')
  OK_END            = openImage('ok_end.png')
  CANCEL            = openImage("cancel.png")
  TAB_RESET         = openImage("tab_reset.png")
  ALCHEMY_TAB       = openImage("alchemy_tab.png")
  EXTRACT_UP        = openImage("extract_up.png")
  CONFIRM           = openImage("confirm.png")
  BAG               = openImage("bag.png")
  SORT              = openImage("sort.png")
  ENHANCE_STAR      = openImage("star.png")
  ENHANCE_ENHANCE   = openImage("enhance.png")
  ENHANCE_OK        = openImage("e_ok.png")

  PINEDEER1         = openImage("pinedeer1.png")
  PINEDEER2         = openImage("pinedeer2.png")
  BEFUDDLE1         = openImage("befuddle1.png")
  BEFUDDLE2         = openImage("befuddle2.png")
  MONTO             = openImage("monto.png")
  MONTO2            = openImage("monto2.png")
  DRONE_A           = openImage("drone_a.png")
  DRONE_B           = openImage("drone_b.png")
  FOREBERION        = openImage("foreberion.png")
  ASCENDION         = openImage("mob.png")
  IRONSHOT1         = openImage("ironshot1.png")
  IRONSHOT2         = openImage("ironshot2.png")
  FIRE_SPIRIT       = openImage("fire_spirit.png")
  FIRE_SPIRIT2      = openImage("fire_spirit2.png")
  DIAMOND_GUARDIAN1 = openImage("diamond_guardian1.png")
  DIAMOND_GUARDIAN2 = openImage("diamond_guardian2.png")
  ALLEY3_MOB        = openImage("alley3_mob.png")
  ALLEY3_MOB2       = openImage("alley3_mob2.png")
  SUMMER5_MOB       = openImage("crane_left.png")
  SUMMER5_MOB2      = openImage("crane_right.png")
  EBON_MAGE1        = openImage("ebon_mage1.png")
  EBON_MAGE2        = openImage("ebon_mage2.png")
  LIMINIA_ICON      = openImage("liminia_icon.png")
  CERNIUM_ICON      = openImage("cernium_icon.png")
  BURNIUM_ICON      = openImage("burnium.png")
  ARCUS_ICON        = openImage("arcus.png")
  ODIUM_ICON        = openImage("odium_icon.png")
  SHANGRILA_ICON    = openImage("shangrila_icon.png")
  ARTERIA_ICON      = openImage("arteria_icon.png")
  VANISHING_ICON    = openImage("vanishing_icon.png")
  CHUCHU_ICON       = openImage("chuchu_icon.png")
  ARCANA_ICON       = openImage("arcana_icon.png")
  MOONBRIDGE_ICON   = openImage("moonbridge_icon.png")
  LACH_ICON         = openImage("lach_icon.png")
  REVERSE_ICON      = openImage("reverse_icon.png")
  RUNE_MINIMAP      = openImage("rune_minimap.png")
  BOUNTY_MINIMAP    = openImage("bounty_minimap.png")
  MINIMAP           = openImage("minimap.png")
  ELITE_BOX         = openImage("elite_box.png")
  PERSON            = openImage("person.png")
  GUILD_PERSON      = openImage("guild_person.png")
  CASH_TAB          = openImage("cash_tab.png")
  ELITE_BOSS_HP     = openImage("elite_boss_hp.png")
  REFRESH_BOSS      = openImage("refresh_boss.png")

  # Auto familiar leveling
  SETUP             = openImage("setup.png")
  SAVE1366              = openImage("save.png")

  # Login to characters for 1 hour
  REBOOT            = openImage("reboot.png")
  SETTING           = openImage("setting.png")

  # TOF
  TAKENO            = openImage("takeno.png")
  IBARAKI           = openImage("ibaraki.png")
  ASK               = openImage("ask.png")
  NEXT              = openImage("next.png")
  YES               = openImage("yes.png")
  TOF_COMPLETE      = openImage("tof_complete.png")
  TOF_BOARD         = openImage("tof_board.png")
  WHITE_QUEST_BULB  = openImage("white_quest_bulb.png")
  MY_LEVEL_RANGE    = openImage("my_level_range.png")
  # WAP
  WAP               = openImage("wap.png")
  WAP_BUFF          = openImage("wap_buff.png")
  # FAM FUEL
  FAM_FUEL          = openImage("fam_fuel.png")
  FAM_BUFF          = openImage("fam_buff.png")
  MILK              = openImage("milk.png")

  # Boss  
  LUCID             = openImage("lucid.png")
  WILL              = openImage("will.png")

  # Cubing  
  CUBE_RESULT       = openImage("cube_result.png")
  ONEMORETRY        = openImage("one_more_try.png")
  ATT_INCREASE      = openImage("att_increase.png")
  EPIC_POT          = openImage("epic_pot.png")

  # Stats TODO: get the actual images
  MAGIC_ATTACk      = openImage("magic_attack.png")
  ATTACK            = openImage("attack.png")
  ALL               = openImage("all_stat.png")
  DEX               = openImage("dex.png")
  STR               = openImage("str.png")
  INT               = openImage("int.png")
  LUK               = openImage("luk.png")
  CRIT_DMG          = openImage("dex.png") # TODO: crit dmg pic
  BOSS              = openImage("boss_dmg.png")
  IED               = openImage("ied.png")
  MESO_OBTAINED     = openImage("meso_obtained.png")
  ITEM_DROP         = openImage("item_drop.png")

  # Familiar
    # Speific Familiars - Ascendion
  FAM_ASCENDION     = openImage("fam_ascendion.png")
  FAM_ASCENDION_NAME = openImage("fam_ascendion_name.png")
  FAM_25_STACK      = openImage("fam_25_stack.png")
  FAM_50_STACK      = openImage("fam_50_stack.png")
  FAM_75_STACK      = openImage("fam_75_stack.png")
  FAM_100_STACK     = openImage("fam_100_stack.png")
  FAM_25_STACK_RARE = openImage("fam_25_stack_rare.png")
  FAM_50_STACK_RARE = openImage("fam_50_stack_rare.png")
  FAM_100_STACK_RARE = openImage("fam_100_stack_rare.png")
    # Specific Famliars - Foreberion
  FAM_FOREBERION    = openImage("fam_foreberion.png")

  FAM_EQUIP         = openImage("fam_equip.png")
  FAM_FUSION        = openImage("fam_fusion.png")
  FAM_STOP          = openImage("fam_stop.png")
  FAM_CANCEL        = openImage("fam_cancel.png")
  FAM_LEVEL5        = openImage("fam_level_5.png")
  FAM_SELECT_ALL    = openImage("fam_select_all.png")
  FAM_FUSE_ACTIVE   = openImage("fam_fuse_active.png")
  FAM_RANK_UP       = openImage("fam_rank_up.png")
  FAM_RARE_FULL_POINTS = openImage("fam_rare_full_points.png")
  FAM_EPIC_FULL_POINTS = openImage("fam_epic_full_points.png")
  FAM_0_POINTS      = openImage("fam_0_points.png")
  FAM_25_POINTS     = openImage("fam_25_points.png")
  FAM_50_POINTS     = openImage("fam_50_points.png")
  FAM_0_150_POINTS  = openImage("fam_0_150_points.png")
  FAM_50_150_POINTS = openImage("fam_50_150_points.png")
  FAM_75_150_POINTS = openImage("fam_75_150_points.png")
  FAM_100_150_POINTS = openImage("fam_100_150_points.png")

  # GREATCARE
  greatcare_play    = openImage("greatcare_play.png")
  greatcare_next    = openImage("greatcare_next.png")

  # Spielgmann Potion
  spieglmann_pot = openImage("spieglmann_pot.png")
  spieglmann_storm_pot = openImage("spieglmann_storm_pot.png")
  spieglmann_growth_pot = openImage("spieglmann_growth_pot.png")
  
  # CR
  CR_BATTLE = openImage("cr_battle.png")
  CR_OK = openImage("cr_ok.png")

  class POE_Images:
    # Currency Tab
    highlight = openImage("highlight.png")
    inactive_transmute = openImage("inactive_transmute.png")
    inactive_alt = openImage("inactive_alt.png")
    inactive_aug = openImage("inactive_aug.png")
    inactive_regal = openImage("inactive_regal.png")
    inactive_scour = openImage("inactive_scour.png")
    inactive_exalt = openImage("inactive_exalt.png")
    inactive_annul = openImage("inactive_annul.png")
    inactive_chaos = openImage("inactive_chaos.png")
    chat_local_tab = openImage("chat_local_tab.png")
    poe_window_x = openImage("poe_window_x.png")
    
    # Cluster
    glowing = openImage("glowing.png") # t1 es
    glimmering = openImage("glimmering.png") # t2 es
    powerful = openImage("powerful.png") # t1 effect
    potent = openImage("potent.png") # t2 effect
    prodigy = openImage("prodigy.png") # t1 int
    bear = openImage("bear.png") # t1 str
    meteor = openImage("meteor.png") # t1 attribute
    sky = openImage("sky.png") # t2 attribute
    kaleidoscope = openImage("kaleidoscope.png") # t1 all res
    salamander = openImage("salamander.png") # t2 fire res
    drake = openImage("drake.png") # t1 fire res

    # Flask
    abecedarian = openImage("abecedarian.png") # 25% effect
    dabbler = openImage("dabbler.png") # 25% effect
    alchemist = openImage("alchemist.png") # 25% effect

    dove = openImage("dove.png") # attack speed
    rainbow = openImage("rainbow.png") # ele res
    impala = openImage("impala.png") # evasion
    owl = openImage("owl.png") # curse
    cheetah = openImage("cheetah.png") # movement speed
    armadillo = openImage("armadillo.png") # armour
    bogmoss = openImage("bogmoss.png") # avoid shock

    granite = openImage("granite.png")
    jade = openImage("jade.png")
    bismuth = openImage("bismuth.png")
    quicksilver = openImage("quicksilver.png")
    amethyst = openImage("amethyst.png")
    topaz = openImage("topaz.png")
    sapphire = openImage("sapphire.png")

    # Other
    mana40 = openImage("mana40.png")
    mana40wide = openImage("mana40wide.png")
    hp60 = openImage("hp60.png")
    hp60wide = openImage("hp60wide.png")
    showcase_empty = openImage("showcase_empty.png")
    helmet_tab = openImage("helmet_tab.png")
    currency_tab = openImage("currency_tab.png")
    
    
  # POE
  POE = POE_Images
  
  def get(key, suffix):
    return getattr(Images, f"{key}{suffix}")
  
  
class Audio:
  TYLER1_AUTISM     = "images/tyler1autism.mp3"
  PING              = "images/ping.mp3"
  AMOGUS            = "images/amogus.mp3"
  AUGH              = "images/augh.mp3"
  BRUH              = "images/bruh.mp3"
  LETMEDOITFORYOU   = "images/let me do it for you.mp3"
  TYLER1_MACHINEGUN = "images/t1 machine.mp3"
  WHYAREYOUGAY      = "images/why are you gay.mp3"
  RETRO_NOTIFICATION = "images/retro_ping.wav"
  
  def get_random_rune_audio():
    return random.choice([Audio.AMOGUS, Audio.AUGH, Audio.BRUH, Audio.LETMEDOITFORYOU, Audio.WHYAREYOUGAY])
#endregion ASSESTS

#region LISTENER
'''
This class is used to listen for key presses and releases. It uses the interception library to do so.
If the key pressed is a key that we are listening for, then we call the callback function associated with that key and also not send the key to the OS. (Like we never pressed it)
Avoid popular libaries like pyautogui, keyboard, pynput, etc. because they use virtual keycodes which are different from the actual keycodes that the OS uses. (Can be detectable by other anticheat but I doubt MS cares)
'''
class KeyListener:
  
  def __init__(self, data):
    self.data = data
    self.events = {}

  def add(self, key, cb):
    self.events[KEYBOARD_MAPPING[key]] = cb

  def beginListeningForPresses(self):
    context = interception.Interception()
    context.set_filter(context.is_keyboard, interception.FilterKeyState.FILTER_KEY_DOWN)
    while True:
      if self.data['stop_flag']:
        return
      
      device = context.wait()
      stroke = context.receive(device)

      if stroke.code in self.events:
        self.events[stroke.code]()
      else:
        context.send(device, stroke)

  def beginListeningForReleases(self):
    context = interception.Interception()
    context.set_filter(context.is_keyboard, interception.FilterKeyState.FILTER_KEY_DOWN)
    while True:
      if self.data['stop_flag']:
        return
      
      device = context.wait()
      stroke = context.receive(device)

      if not stroke.code in self.events:
        context.send(device, stroke)

  def run(self):
    t1 = threading.Thread(target=self.beginListeningForPresses)
    t1.start()
    t2 = threading.Thread(target=self.beginListeningForReleases)
    t2.start()
#endregion LISTENER

#region DISCORD REQUEST
load_dotenv()

abort = False
API_KEY = os.getenv('FLASK_KEY_API')

def get_URL():
  useLocalServer = "dev" in sys.argv or state['localserver']
  return "http://localhost:5000" if useLocalServer else "https://ms-discord-bot-fd16a56d7c26.herokuapp.com"
  

def send_non_block(reqFn):
  if abort or not state['sendstatus']: 
    return
  t = threading.Thread(target=reqFn)
  t.start()

def post_status(route, data={ "user": "jeemong" }):
  URL = get_URL()
  def post_status_helper():
    print(f"Posting status to {URL}/{route}")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.post(f"{URL}/{route}", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/{route}: {e}")
  send_non_block(post_status_helper)

def get_status(route, data={ "user": "jeemong" }):
  URL = get_URL()
  def get_status_helper():
    print(f"Getting status to {URL}/{route}")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.get(f"{URL}/{route}", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/{route}: {e}")
  send_non_block(get_status_helper)

def post_fam_level(data):
  URL = get_URL()
  def post_fam_level_helper():
    print(f"Posting status to {URL}/fam_level")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.post(f"{URL}/fam_level", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/fam_level: {e}")
  # send_non_block(post_fam_level_helper)

def post_tof(data):
  URL = get_URL()
  def post_tof_helper():
    print(f"Posting status to {URL}/tof")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.post(f"{URL}/tof", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/tof: {e}")
  # send_non_block(post_tof_helper)

def post_wap(data):
  URL = get_URL()
  def post_wap_helper():
    print(f"Posting status to {URL}/wap")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.post(f"{URL}/wap", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/wap: {e}")
  # send_non_block(post_wap_helper)

def post_fam_fuel(data):
  URL = get_URL()
  def post_fam_fuel_helper():
    print(f"Posting status to {URL}/fam_fuel")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      requests.post(f"{URL}/fam_fuel", headers=headers, json=data)
    except Exception as e:
      print(f"Error posting status to {URL}/fam_fuel: {e}")
  # send_non_block(post_fam_fuel_helper)
    
def post_summary(start_time, user):
  URL = get_URL()
  def post_summary_helper():
    print(f"Posting bot run time to {URL}/summary")
    headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
    try:
      if start_time is None:
        raise Exception("Start time is None")
      requests.post(f"{URL}/summary", headers=headers, json={ "user": user, "start_time": datetime.timestamp(start_time), "end_time": datetime.timestamp(datetime.now()) })
    except Exception as e:
      print(f"Error posting time to {URL}/summary: {e}")
  send_non_block(post_summary_helper)
#endregion DISCORD REQUEST


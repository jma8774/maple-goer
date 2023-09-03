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

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')

#region BOTBASE
START_KEY = 'f7'
PAUSE_KEY = 'f8'
RESET_LOOT_TIMER_KEY = 'f9'
minimap_rune_region = (0, 0, 200, 200)

class BotBase:
  def __init__(self, data, config):
    self.data = data
    self.config = config
    self.thread = None

    self.setup_data()
    self.setup_audio()

    # Interception Setup for main loop
    kdevice = interception.listen_to_keyboard()
    mdevice = interception.listen_to_mouse()
    interception.inputs.keyboard = kdevice
    interception.inputs.mouse = mdevice
    clear()

    # Interception Key Listener Setup (seperate thread)
    kl = KeyListener(data)
    kl.add(PAUSE_KEY, self.pause)
    kl.add(START_KEY, self.start)
    kl.add(RESET_LOOT_TIMER_KEY, self.reset_loot_timer)
    kl.run()

    self.commands()

  def setup_data(self):
    self.data['stop_flag'] = False
    self.data['is_paused'] = True
    self.data['duration_paused'] = 0
    self.data['time_started'] = None

    self.data['next_loot'] = datetime.now() + timedelta(minutes=1.7)
    self.data['is_changed_map'] = False
    self.data['key_pressed'] = {}
    self.data['rune_playing'] = False
    self.data['next_rune_check'] = datetime.now()
    self.data['next_elite_box_check'] = datetime.now()
    self.data['someone_on_map'] = False

  def run(self):
    if "script" not in self.config:
      raise Exception("Config must have script functions")
    setup = self.config['setup'] if 'setup' in self.config else None
    script = self.config['script']
    
    try:
      while True:
        if self.data['is_paused'] == True:
          if self.data['duration_paused'] > 60:
            print("Bot has been paused for 3 minutes, ending current session and posting to discord")
            self.data['duration_paused'] = float('-inf')
            self.post_running_time()
          time.sleep(1)
          self.data['duration_paused'] += 1
          continue
        
        if self.data['time_started'] == None:
          post_status("started")
          self.data['time_started'] = datetime.now()
        self.data['duration_paused'] = 0

        # Setup for each new run
        if setup:
          setup()
        self.thread = threading.Thread(target=script)
        self.thread.start()
        self.thread.join()
        self.release_all()

        # Play sound if whiteroomed
        if self.data['is_changed_map']:
          print(f"Map change detected, script paused, playing audio: Press {PAUSE_KEY} to stop")
          post_status("whiteroom")
          self.play_audio(Audio.TYLER1_AUTISM)
    except KeyboardInterrupt:
      self.data['stop_flag'] = True
      self.post_running_time()
      print("Exiting... (Try spamming CTRL + C)")
  
  def check_rune(self):
    if datetime.now() > self.data['next_rune_check']:
      if pag.locateOnScreen(Images.RUNE_MINIMAP, confidence=0.7, region=minimap_rune_region):
        if not self.data['rune_playing']:
          self.play_audio(Audio.get_random_rune_audio())
          self.data['rune_playing'] = True
        post_status("rune")
      self.data['next_rune_check'] = datetime.now() + timedelta(seconds=45)

  def check_person_entered_map(self):
    if pag.locateOnScreen(Images.PERSON, region=minimap_rune_region):
      if not self.data['someone_on_map']:
        post_status("someone_entered_map")
        self.data['someone_on_map'] = True
    else:
      self.data['someone_on_map'] = False

  def check_elite_box(self, boxkey='f6'):
    cur = datetime.now()
    if cur > self.data['next_elite_box_check']:
      boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
      while boxloc != None:
        self.press_release(boxkey)
        boxloc = pag.locateCenterOnScreen(Images.ELITE_BOX, confidence=0.9)
      self.data['next_elite_box_check'] = cur + timedelta(seconds=45)

  def post_running_time(self, user="jeemong"):
    if self.data['time_started'] != None:
      post_summary(self.data['time_started'], user)
      self.data['time_started'] = None
    
  def pause(self):
    print('Pausing')
    self.data['is_paused'] = True
    self.data['rune_playing'] = False
    self.data['x_and_down_x'] = True
    if 'pause_cb' in self.data:
      self.data['pause_cb']()
    self.pause_audio()

  def start(self):
    print('\nStarting')
    self.data['is_paused'] = False
    self.data['is_changed_map'] = False

  def reset_loot_timer(self):
    print('\nResetting loot timer')
    self.data['next_loot'] = datetime.now() + timedelta(minutes=1.7)

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
      if self.data['key_pressed'][key]:
        self.release(key)

  def press(self, key, delay=0.05):
    interception.key_down(key)
    self.data['key_pressed'][key] = True
    time.sleep(delay)
    
  def release(self, key, delay=0.05):
    interception.key_up(key)
    self.data['key_pressed'][key] = False
    time.sleep(delay)

  def press_release(self, key, delay=0.05):
    self.press(key)
    self.release(key, delay)

  def commands(self):
    print(f"Using images for resolution of 1366 fullscreen maplestory")
    print("Commands:")
    print(f"  {START_KEY} - start")
    print(f"  {PAUSE_KEY} - pause")
    print(f"  {RESET_LOOT_TIMER_KEY} - reset loot timer")
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
  EXTRACT_UP        = openImage("extract_up.png")
  CONFIRM           = openImage("confirm.png")
  BAG               = openImage("bag.png")
  SORT              = openImage("sort.png")
  ENHANCE_STAR      = openImage("star.png")
  ENHANCE_ENHANCE   = openImage("enhance.png")
  ENHANCE_OK        = openImage("e_ok.png")

  MONTO             = openImage("monto.png")
  MONTO2            = openImage("monto2.png")
  DRONE_A           = openImage("drone_a.png")
  DRONE_B           = openImage("drone_b.png")
  FOREBERION        = openImage("foreberion.png")
  ASCENDION         = openImage("mob.png")
  LIMINIA_ICON      = openImage("liminia_icon.png")
  REVERSE_ICON      = openImage("reverse_icon.png")
  RUNE_MINIMAP      = openImage("rune_minimap.png")
  BOUNTY_MINIMAP    = openImage("bounty_minimap.png")
  MINIMAP           = openImage("minimap.png")
  ELITE_BOX         = openImage("elite_box.png")
  PERSON            = openImage("person.png")

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
URL = "https://ms-discord-bot-fd16a56d7c26.herokuapp.com"
# URL = "http://localhost:5000"
API_KEY = os.getenv('FLASK_KEY_API')

def post_status(route, data={ "user": "jeemong" }):
  print(f"Posting status to {URL}/{route}")
  headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
  try:
    requests.post(f"{URL}/{route}", headers=headers, json=data)
  except Exception as e:
    print(f"Error posting status to {URL}/{route}: {e}")

def get_status(route, data={ "user": "jeemong" }):
  print(f"Getting status to {URL}/{route}")
  headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
  try:
    requests.get(f"{URL}/{route}", headers=headers, json=data)
  except Exception as e:
    print(f"Error posting status to {URL}/{route}: {e}")
    
def post_summary(start_time, user):
  print(f"Posting bot run time to {URL}/summary")
  headers = {'X-API-Key': API_KEY, 'Content-Type': 'application/json'}
  try:
    if start_time is None:
      raise Exception("Start time is None")
    requests.post(f"{URL}/summary", headers=headers, json={ "user": user, "start_time": datetime.timestamp(start_time), "end_time": datetime.timestamp(datetime.now()) })
  except Exception as e:
    print(f"Error posting time to {URL}/summary: {e}")
#endregion DISCORD REQUEST

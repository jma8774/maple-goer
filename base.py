from PIL import Image
import random
import threading
import interception
from interception._keycodes import KEYBOARD_MAPPING
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

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
  
  def __init__(self, stop_flag):
    self.stop_flag = stop_flag
    self.events = {}

  def add(self, key, cb):
    self.events[KEYBOARD_MAPPING[key]] = cb

  def beginListeningForPresses(self):
    context = interception.Interception()
    context.set_filter(context.is_keyboard, interception.FilterKeyState.FILTER_KEY_DOWN)
    while True:
      if self.stop_flag[0]:
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
      if self.stop_flag[0]:
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
# URL = "https://ms-discord-bot-fd16a56d7c26.herokuapp.com"
URL = "http://localhost:5000"
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

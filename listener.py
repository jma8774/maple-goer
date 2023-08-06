import threading
import interception
from interception._keycodes import KEYBOARD_MAPPING

'''
This class is used to listen for key presses and releases. It uses the interception library to do so.
If the key pressed is a key that we are listening for, then we call the callback function associated with that key and also not send the key to the OS. (Like we never pressed it)
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
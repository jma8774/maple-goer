import interception
from base import KeyListener, Images
import time
import pyautogui as pag
import threading
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import signal
import sys
import pyperclip as pc


Images = Images.POE2

START_KEY = 'f7'
PAUSE_KEY = 'f8'

ITEMS_TO_BUY = {
  "withered_wand": Images.withered_wand_focused,
  "gemini_bow": Images.gemini_bow_focused,
  "dueling_wand": Images.dueling_wand_focused,
  "galvanic_wand": Images.galvanic_wand_focused,
  "overseer_tablet": Images.overseer_focused,
}

# Flask app setup
app = Flask(__name__)
load_dotenv()
FLASK_TOKEN = os.getenv('FLASK_KEY_API', 'default_api_key')

# Global buyer instance
buyer_instance = None

# Main POE2Buyer class with API capabilities
class POE2Buyer:
  def __init__(self):
    # Interception setup for main loop
    kdevice = interception.listen_to_keyboard()
    mdevice = interception.listen_to_mouse()
    interception.inputs.keyboard = kdevice
    interception.inputs.mouse = mdevice
    self.interception = interception

    # Status tracking for API
    self.running = True 
    self.stop_flag = False
    self.current_item = None
    self.reset_item_to_buy_timer = datetime.now()

    # Shared data for KeyListener
    self.data = {
      'running': self.running,
      'stop_flag': self.stop_flag
    }
    
    kl = KeyListener(self.data)
    kl.add(START_KEY, self.start)
    kl.add(PAUSE_KEY, self.pause)
    kl.run()

    # Thread control
    self.buyer_thread = None
    
    # Start the buyer loop immediately
    self.buyer_thread = threading.Thread(target=self.run_background, daemon=True)
    self.buyer_thread.start()
    print("POE2 Buyer API started automatically")

  def start(self):
    self.running = True
    print("POE2 Buyer started")
  
  def pause(self):
    self.running = False
    print("POE2 Buyer paused")
  
  def shutdown(self):
    """Gracefully shutdown the buyer"""
    print("Shutting down POE2 Buyer [running=False] [stop_flag=True]...")
    self.stop_flag = True
    self.running = False
    
    # Update shared data for KeyListener
    self.data['stop_flag'] = True
    self.data['running'] = False
    
    # Wait for the buyer thread to finish
    if self.buyer_thread and self.buyer_thread.is_alive():
      print("Waiting for buyer thread to finish...")
      self.buyer_thread.join(timeout=5)
    
    print("POE2 Buyer shutdown complete")

  def press(self, key, delay=0.05):
    self.interception.key_down(key)
    if delay > 0:
      time.sleep(delay)
    
  def release(self, key, delay=0.05):
    self.interception.key_up(key)
    if delay > 0:
      time.sleep(delay)

  def press_release(self, key, delay=0.05, pressdelay=0.05):
    self.press(key, pressdelay)
    self.release(key, delay)

  def moveto(self, location, delay=0.05):
    self.interception.move_to(location)
    if delay > 0:
      time.sleep(delay)

  def click(self, location=None, delay=0.05):
    if (location == None):
      self.interception.click()
    else:
      self.interception.click(location)
    if delay > 0:
      time.sleep(delay)

  def get_image_location(self, name, img, region=(0, 0, 2560, 1440), confidence=0.95):
    def locate():
      if confidence == None:
        return pag.locateOnScreen(img, region=region)
      else:
        return pag.locateOnScreen(img, confidence=confidence, region=region)
      
    loc = locate()
    if not loc:
      return None
    return loc

  def check_timer(self):
    if self.current_item != None and self.reset_item_to_buy_timer < datetime.now():
      print(f"Item to buy set to: None")
      self.current_item = None

  def buy_highlighted_item(self):
    try:
      self.check_timer()
      
      if not self.current_item or self.current_item['item_to_buy_name'] not in ITEMS_TO_BUY:
        return
      
      # Wait for merchant header to be visible
      loc = self.get_image_location("poe2_merchant", Images.poe2_merchant, region=(751, 185, 881-751, 228-185), confidence=0.9)
      while not loc and self.current_item != None:
        self.check_timer()
        loc = self.get_image_location("poe2_merchant", Images.poe2_merchant, region=(751, 185, 881-751, 228-185), confidence=0.9)
        time.sleep(0.01)
      if not loc:
        print(f"No merchant header found")
        return
      print(f"Found merchant header")
      
      self.moveto((100, 100), delay=0.01)

      # Ctrl F and Backspac
      self.press('ctrl', delay=0.01)
      self.press_release('f', delay=0.01)
      self.press_release('f', delay=0.01)
      self.release('ctrl', delay=0.01)
      self.press_release('backspace', delay=0.01)
      self.press_release('backspace', delay=0.01)

      # Paste the regex in
      pc.copy(self.current_item['search_regex'])
      self.press('ctrl', delay=0.01)
      self.press('v', delay=0.01)
      self.release('ctrl', delay=0.01)
      self.release('v', delay=0.05)
      
      for _ in range(2):
        img = ITEMS_TO_BUY[self.current_item['item_to_buy_name']]
        loc = self.get_image_location(self.current_item['item_to_buy_name'], img, region=(376, 173, 1300-376, 1174-173), confidence=None)
        if loc:
          self.moveto((loc.left+5, loc.top+5), delay=0)
          self.moveto(loc, delay=0.01)
          self.press('ctrl', delay=0.01)
          self.click(loc, delay=0.01)
          self.click(loc, delay=0.01)
          self.release('ctrl', delay=0.01)
          self.release('ctrl', delay=0.01)
          self.moveto((100, 100), delay=0.01)
      self.current_item = None
      print(f"Item to buy set to: None")
    except Exception as e:
      print(f"Error in buy_highlighted_item: {e}")
  
  def run_background(self):
    """Background run method for API mode"""
    try:
      print("POE2 Buyer started in background mode...")
      while not self.stop_flag:
        if self.running:
          self.buy_highlighted_item()
          time.sleep(0.05)
        else:
          time.sleep(0.5)
    except Exception as e:
      print(f"Background run error: {e}")
    finally:
      print("POE2 Buyer background thread stopped")


# Flask API error handlers and middleware
@app.errorhandler(Exception) 
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@app.before_request
def before_request():
    def ok():
        return request.path in ["/hello", "/buy"]
    if not ok():
        return "Invalid path", 400
    key = request.headers.get('x-api-key')
    if key != FLASK_TOKEN:
        print(f"Invalid API key: {key}, needs to be {FLASK_TOKEN}")
        return "Invalid API key", 401
        


# Flask API Routes
@app.route('/hello', methods=['GET'])
def handle_hello():
    return jsonify({"message": "POE2 Buyer API is running", "timestamp": datetime.now().isoformat()}), 200

@app.route('/buy', methods=['POST'])
def handle_buy():
    data = request.json
    item_to_buy_name = data.get('item_to_buy_name')
    price = data.get('price')
    search_regex = data.get('search_regex')
    if item_to_buy_name and item_to_buy_name in ITEMS_TO_BUY:
        buyer_instance.reset_item_to_buy_timer = datetime.now() + timedelta(seconds=15)
        buyer_instance.current_item = {
            "item_to_buy_name": item_to_buy_name,
            "price": price,
            "search_regex": search_regex
        }
        print(f"Item to buy configured to: {item_to_buy_name} with price: {price} [regex={search_regex}]")
    return jsonify({"message": "Item to buy configured to: " + item_to_buy_name}), 200

def signal_handler(sig, frame):
    """Handle Ctrl+C (SIGINT) gracefully"""
    global buyer_instance
    print(f"\nReceived signal {sig} - shutting down...")
    
    if buyer_instance:
        buyer_instance.shutdown()
    
    print("Exiting...")
    sys.exit(0)

def run_api_server(host='0.0.0.0', port=5001):
    """Run the Flask API server"""
    global buyer_instance
    
    # Set up signal handlers BEFORE creating buyer instance
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    buyer_instance = POE2Buyer()
    print(f"Starting POE2 Buyer API server on {host}:{port}")
    print("Available endpoints:")
    print(f"  GET /hello - Health check")
    print(f"\nAPI Key required for /configure endpoint")
    print(f"Use header: x-api-key: {FLASK_TOKEN}")
    print(f"\nThe buyer starts automatically and runs continuously.")
    print(f"Use F7 to start/resume and F8 to pause the buyer.")
    print(f"Press Ctrl+C to shutdown gracefully.")
    
    try:
        # Disable Flask's signal handling so our handler works
        app.run(host=host, port=port, debug=False, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt caught in Flask")
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"Flask app error: {e}")
        if buyer_instance:
            buyer_instance.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    try:
        port = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5001
        run_api_server(port=port)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt in main")
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if buyer_instance:
            buyer_instance.shutdown()
        sys.exit(1)
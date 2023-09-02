import os
from web import app
from bot import runClient
from threading import Thread

port = int(os.getenv("PORT", 5000))

if __name__ == '__main__':
  try:
    # Run Flask to handle HTTP requests 
    # Need to run it on a thread because it is blocking
    flaskThread = Thread(target=lambda: app.run(use_reloader=False, debug=False, host="0.0.0.0", port=port))
    flaskThread.daemon = True
    flaskThread.start()

    # Run Discord bot on main thread
    runClient(port)

    exit()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    exit()

def exit():
  os._exit(1)
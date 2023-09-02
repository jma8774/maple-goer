import os
from dotenv import load_dotenv
from web import app
from bot import client
from threading import Thread

if __name__ == '__main__':
  try:
    # Run Flask to handle HTTP requests 
    # Need to run it on a thread because it is blocking
    flaskThread = Thread(target=lambda: app.run(use_reloader=False, debug=False, host="0.0.0.0", port=os.environ.get("PORT", 5000)))
    flaskThread.daemon = True
    flaskThread.start()

    # Run Discord bot on main thread
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    print("DISCORD TOKEN:", TOKEN)
    client.run(TOKEN)

    exit()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    exit()

def exit():
  os._exit(1)
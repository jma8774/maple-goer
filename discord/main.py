import asyncio
import os
from dotenv import load_dotenv
from web import app
from bot import client
from threading import Thread

if __name__ == '__main__':
  try:
    # Run Flask to handle HTTP requests 
    flaskThread = Thread(target=lambda: app.run(use_reloader=False))
    flaskThread.daemon = True
    flaskThread.start()

    # Run Discord bot on main thread
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    client.run(TOKEN)

    exit()
  except KeyboardInterrupt:
    print("Exiting... (Try spamming CTRL + C)")
    exit()

def exit():
  os._exit(1)
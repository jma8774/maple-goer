import discord
from dotenv import load_dotenv
import os

client = discord.Client(intents=discord.Intents.default())
channels = {}
users = {}
isDebug = False

@client.event
async def on_ready():
  global channels, users
  print(f'{client.user} has connected to Discord!')
  channels = {
    "lounge": client.get_channel(420679175465336832),
    "bot-spam": client.get_channel(1018050116424306738),
  }
  users = {
    "ricky": "600922329815449632",
    "justin": "152956804270129152",
    "jeemong": "152957206025863168",
  }

async def send(channel, message, user=None):
  global channels, isDebug
  print(f"Sending message to {channel}: {message}")
  debug = "**[Debug]** " if isDebug else ""
  if user:
    await channels[channel].send(debug + f"<@{users[user]}> " + message)
  else:
    await channels[channel].send(debug + message)

def runClient(port):
  global isDebug
  isDebug = port == 5000
  load_dotenv()
  TOKEN = os.getenv('DISCORD_TOKEN')
  client.run(TOKEN)
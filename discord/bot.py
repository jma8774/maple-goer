import discord

client = discord.Client(intents=discord.Intents.default())
channels = {}
users = {}

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
  print(f"Sending message to {channel}: {message}")
  global channels
  if user:
    await channels[channel].send(f"<@{users[user]}> " + message)
  else:
    await channels[channel].send(message)
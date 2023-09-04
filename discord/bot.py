import discord
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz


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

async def sendSummary(channel, data):
  global channels, isDebug
  print(f"Sending summary embed to {channel}: {data}")
  debug = "**[Debug]** " if isDebug else ""

  data['start_time'] = estTime(datetime.fromtimestamp(data['start_time']))
  data['end_time'] = estTime(datetime.fromtimestamp(data['end_time']))

  duration = (data['end_time'] - data['start_time']).total_seconds()
  mph = 420000000
  mesos = format(int(duration * (mph / 3600)), ",")
  nodes = format(int(duration * (15 / 3600)), ",")

  embed = discord.Embed(
      title="Summary", 
      description=f"Hey <@{users[data['user']]}>, here are some stats from your latest session!", 
      color=0x00ff00,
      timestamp=data['end_time'],
    )
  
  embed.add_field(name="\u200b", value="\u200b", inline=False)
  embed.add_field(name="**:clock1: Start Time**", value=f"{dtFormat(data['start_time'])} EST")
  embed.add_field(name="**:clock9: Stop Time**", value=f"{dtFormat(data['end_time'])} EST")
  duration_str = secondsToDisplay(duration)
  if duration_str:
    embed.add_field(name="**:hourglass: Duration**", value=duration_str)
  embed.add_field(name="**:moneybag: Mesos Earned**", value=f"{mesos}")
  embed.add_field(name="**:gem: Nodes Earned**", value=f"{nodes}")
  embed.add_field(name="\u200b", value="\u200b", inline=False)

  await channels[channel].send(debug+f"<@{users[data['user']]}>", embed=embed)

def secondsToDisplay(secs):
    hours = int(secs // 3600)
    mins = int((secs % 3600) // 60)
    s = ""
    if hours > 0:
        s += f"{hours} {'hours' if hours > 1 else 'hour'} "
    if mins > 0:
        s += f"{mins} {'minutes' if mins > 1 else 'minute'} "
    return s.strip()

def estTime(dt):
  return dt.astimezone(pytz.timezone('America/New_York'))

def dtFormat(dt):
  return dt.strftime('%H:%M:%S')

def runClient(port):
  global isDebug
  isDebug = port == 5000
  load_dotenv()
  TOKEN = os.getenv('DISCORD_TOKEN')
  client.run(TOKEN)
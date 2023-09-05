import discord
from discord.utils import get
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import pytz
from gtts import gTTS
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

guilds = {}
channels = {}
users = {}
isDebug = False

messagesQueue = []

@client.event
async def on_ready():
  global messagesQueue, channels, users
  print(f'{client.user} has connected to Discord!')
  guilds = {
    "apes": client.get_guild(152954629993398272),
  }
  channels = {
    "lounge": client.get_channel(420679175465336832),
    "bot-spam": client.get_channel(1018050116424306738),
    "bot-spam-2": client.get_channel(1148302801961758772),
  }
  users = {
    "ricky": 600922329815449632,
    "justin": 152956804270129152,
    "jeemong": 152957206025863168,
  }
  # Clean up queue every 300 seconds
  while True:
    print("Cleaning up messages queue")
    await asyncio.sleep(300)
    now = datetime.now()
    removed = 0
    for (message, time) in messagesQueue:
      if now < time:
        break
      removed += 1
      await message.delete()
    messagesQueue = messagesQueue[removed:]

async def delete_all_bot_msgs(channel):
  global channels
  print(f"Deleting bot messages in {channel}")
  print(channels[channel].id)
  msgs = await channels[channel].history(limit=100).flatten()
  for msg in msgs:
    print(msg)

async def join_users_channel(userId: int) -> discord.Guild:
  user = client.get_user(userId)
  for guild in client.guilds:
    for channel in guild.voice_channels:
      for member in channel.members:
        if member.id == userId:
          # If I am already in a voice channel, disconnect from it
          connected_to = get(client.voice_clients, guild=guild)
          if connected_to is not None:
            await connected_to.disconnect()

          await channel.connect()
          print(f"I joined {user.name}'s channel at {channel.name}")
          return guild
  print(f"I could not find {user.name} in any channel")
  return None

async def speakToUserId(userId: int, message: str):
  try:
    guild = await join_users_channel(userId)
    if guild is None:
      print("I am not in the specified guild, so I can't speak")
      return
    
    voice_client = get(client.voice_clients, guild=guild)
    if voice_client is None:
      print(f"I am not in a voice channel in guild {guild}, so I can't speak")
      return
    
    print(f"TTS: {message}")
    tts = gTTS(text=message, lang='en')
    tts.save("tts.mp3")
    executable_path = "C:\\Users\\Jimmy\\Desktop\\ffmpeg\\bin\\ffmpeg.exe" if isDebug else "ffmpeg"
    voice_client.play(discord.FFmpegPCMAudio(executable=executable_path, source="tts.mp3"))
  except Exception as e:
    print(f"Error while attempting to speak to user: {e}")

async def speakToName(name, message: str):
  await speakToUserId(users[name], message)

async def send(channel, message, user:str=None, addToQueue=True):
  global channels, isDebug
  print(f"Sending message to {channel}: {message}")
  debug = "**[Debug]** " if isDebug else ""
  messageObj = None
  if user:
    messageObj = await channels[channel].send(debug + f"<@{users[user]}> " + message)
  else:
    messageObj = await channels[channel].send(debug + message)
  if addToQueue and messageObj is not None:
    messagesQueue.append((messageObj, datetime.now() + timedelta(seconds=60)))

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
  tickets = format(int(duration * (5 / 3600)), ",")

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
  embed.add_field(name="**:tickets:  Tickets Earned**", value=f"{tickets}")
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
  return dt.strftime('%I:%M %p').lstrip('0')

def runClient(port):
  global isDebug
  isDebug = port == 5000
  load_dotenv()
  TOKEN = os.getenv('DISCORD_TOKEN')
  client.run(TOKEN)
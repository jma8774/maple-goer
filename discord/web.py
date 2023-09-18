import asyncio
from flask import Flask, request, jsonify
from bot import client, send, sendSummary, speakToName, delete_all_bot_msgs
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz
from common import secondsToDisplay, dtFormat

app = Flask(__name__)

load_dotenv()
TOKEN = os.getenv('FLASK_KEY_API')

@app.errorhandler(Exception) 
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

@app.before_request
def before_request():
    def ok():
        return request.path == "/hello"
    key = request.headers.get('x-api-key')
    if not ok() and key != TOKEN:
        return "Invalid API key", 401

@app.route('/hello', methods=['GET'])
def handle_hello():
    client_event(send("bot-spam-2", "hello!"))
    return "hi!", 200

@app.route('/whiteroom', methods=['POST'])
def handle_whiteroom():
    body = request.json
    client_event(speakToName(body["user"], f"{body['user']} you got whiteroomed you dumbass"))
    client_event(send("bot-spam-2", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam-2", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam-2", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam-2", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam-2", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    return "Success", 200

@app.route('/rune', methods=['POST'])
def handle_rune():
    body = request.json
    client_event(send("bot-spam-2", "Rune is up :robot:", body["user"]))
    return "Success", 200

@app.route('/someone_entered_map', methods=['POST'])
def handle_someone_entered_map():
    body = request.json
    client_event(send("bot-spam-2", "Someone entered your map  <:monkas:421119362225799178> <:monkas:421119362225799178> <:monkas:421119362225799178>", body["user"]))
    return "Success", 200

@app.route('/started', methods=['POST'])
def handle_started():
    body = request.json
    client_event(send("bot-spam-2", f"Started his cousin at :clock1: **{dtFormat(datetime.now())} EST** :clock1:", body["user"], addToQueue=False))
    return "Success", 200

@app.route('/tof', methods=['POST'])
def handle_tof():
    body = request.json
    status, user = body["status"], body["user"]
    if status == "NoBulb":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot couldn't find the white quest bulb", addToQueue=True))
    elif status == "InProgress":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot tried to complete the quest but we need to wait, trying again in 5 minutes", addToQueue=True))
    elif status == "NoPerson":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot couldn't find your npc to click on", addToQueue=True))
    elif status == "NoAsk":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot coulnd't find the ask button", addToQueue=True))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot successfully started a new TOF ask", addToQueue=True))
    elif status == "Done":
        client_event(send("bot-spam-2", f"**[TOF {dtFormat(datetime.now())} EST]** {user}'s bot completed all TOF asks, it will stop asking now", addToQueue=True))
    return "Success", 200

@app.route('/wap', methods=['POST'])
def handle_wap():
    body = request.json
    status, user = body["status"], body["user"]
    if status == "InventoryNotFound":
        client_event(send("bot-spam-2", f"**[WAP {dtFormat(datetime.now())} EST]** {user}'s bot couldn't find the USE inventory", addToQueue=True))
    elif status == "AlreadyWapped":
        client_event(send("bot-spam-2", f"**[WAP {dtFormat(datetime.now())} EST]** {user}'s bot tried to wap, but it is already active", addToQueue=True))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[WAP {dtFormat(datetime.now())} EST]** {user}'s bot used a wap", addToQueue=True))
    elif status == "Failed":
        client_event(send("bot-spam-2", f"**[WAP {dtFormat(datetime.now())} EST]** {user}'s bot failed to use the wap lol", addToQueue=True))
    return "Success", 200

@app.route('/fam_fuel', methods=['POST'])
def handle_fam_fuel():
    body = request.json
    status, user = body["status"], body["user"]
    if status == "InventoryNotFound":
        client_event(send("bot-spam-2", f"**[FAM FUEL {dtFormat(datetime.now())} EST]** {user}'s bot couldn't find the USE inventory", addToQueue=True))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[FAM FUEL {dtFormat(datetime.now())} EST]** {user}'s bot used a familiar fuel", addToQueue=True))
    elif status == "Failed":
        client_event(send("bot-spam-2", f"**[FAM FUEL {dtFormat(datetime.now())} EST]** {user}'s bot failed to use the familiar fuel lol", addToQueue=True))
    return "Success", 200

@app.route('/delete_all_bot_msgs', methods=['POST'])
def handle_delete_all_bot_msgs():
    body = request.json
    client_event(delete_all_bot_msgs(body["channel"]))
    return "Success", 200


# @app.route('/stopped', methods=['POST'])
# def handle_stopped():
#     def secondsToDisplay(secs):
#         hours = int(secs // 3600)
#         mins = int((secs % 3600) // 60)
#         s = ""
#         if hours > 0:
#             s += f"{hours} {'hours' if hours > 1 else 'hour'} "
#         if mins > 0:
#             s += f"{mins} {'minutes' if mins > 1 else 'minute'} "
#         return s.strip()
#     body = request.json
#     mph = 420000000
#     duration = body["duration"]
#     mesos = format(int(duration * (mph / 3600)), ",")
#     client_event(send("bot-spam-2", 
#                       f"Stopped his cousin at :clock1: **{datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S')} EST** :clock1: \n\nAssuming a rate of 420m mesos per hour, they earned {mesos} mesos from this {secondsToDisplay(duration)} long session! :tada: :tada: :tada:", 
#                       body["user"])
#                 )
#     return "Success", 200

@app.route('/summary', methods=['POST'])
def handle_summary():
    data = request.json
    client_event(sendSummary("bot-spam-2", data))
    return "Success", 200

# Discord bot is on another event loop/thread, so we need to use this function to call it's functions IDK TBH BUT IT WORKS
# Flask does not allow us to await the discord client's functions, so we need to use this function to put the discord client's functions on the client's event loop to run asynchronously
def client_event(coro):
    asyncio.run_coroutine_threadsafe(coro, client.loop)
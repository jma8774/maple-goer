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
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin couldn't find the white quest bulb", addToQueue=False))
    elif status == "InProgress":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin tried to complete the quest but we still need to wait, trying again in 5 minutes", addToQueue=False))
    elif status == "NoPerson":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin couldn't find the npc to click on", addToQueue=False))
    elif status == "NoAsk":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin coulnd't find the ask button", addToQueue=False))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin successfully started a new Thread of Fate quest", addToQueue=False))
    elif status == "Done":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - ToF]** {user}'s cousin completed all the Thread of Fate quest, it will stop asking now", addToQueue=False))
    return "Success", 200

@app.route('/wap', methods=['POST'])
def handle_wap():
    body = request.json
    status, user = body["status"], body["user"]
    if status == "InventoryNotFound":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - WAP]** {user}'s cousin couldn't find the USE inventory", addToQueue=False))
    elif status == "AlreadyWapped":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - WAP]** {user}'s cousin tried to WAP, but it is already active", addToQueue=False))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - WAP]** {user}'s cousin used a WAP", addToQueue=False))
    elif status == "Failed":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - WAP]** {user}'s cousin failed to use the WAP", addToQueue=False))
    return "Success", 200

@app.route('/fam_fuel', methods=['POST'])
def handle_fam_fuel():
    body = request.json
    status, user = body["status"], body["user"]
    if status == "InventoryNotFound":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - Familiar Essence]** {user}'s cousin couldn't find the USE inventory", addToQueue=False))
    elif status == "Success":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - Familiar Essence]** {user}'s cousin used a familiar essence", addToQueue=False))
    elif status == "Failed":
        client_event(send("bot-spam-2", f"**[{dtFormat(datetime.now())} EST - Familiar Essence]** {user}'s cousin failed to use the familiar fuel", addToQueue=False))
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
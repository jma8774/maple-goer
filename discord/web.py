import asyncio
from flask import Flask, request, jsonify, abort
from bot import client, send
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

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
    client_event(send("bot-spam", "hello!"))
    return "hi!", 200

@app.route('/whiteroom', methods=['POST'])
def handle_whiteroom():
    body = request.json
    client_event(send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    client_event(send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"]))
    return "Success", 200

@app.route('/rune', methods=['POST'])
def handle_rune():
    body = request.json
    client_event(send("bot-spam", "Rune is up :robot:", body["user"]))
    return "Success", 200

@app.route('/someone_entered_map', methods=['POST'])
def handle_someone_entered_map():
    body = request.json
    client_event(send("bot-spam", "Someone entered your map  <:monkas:421119362225799178> <:monkas:421119362225799178> <:monkas:421119362225799178>", body["user"]))
    return "Success", 200

@app.route('/started', methods=['POST'])
def handle_started():
    body = request.json
    client_event(send("bot-spam", f"Started his bot at :clock1: **{datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S')} EST** :clock1:", body["user"]))
    return "Success", 200

# Discord bot is on another event loop/thread, so we need to use this function to call it's functions IDK TBH BUT IT WORKS
# Flask does not allow us to await the discord client's functions, so we need to use this function to put the discord client's functions on the client's event loop to run asynchronously
def client_event(coro):
    asyncio.run_coroutine_threadsafe(coro, client.loop)
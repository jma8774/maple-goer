import asyncio
from flask import Flask, request, jsonify, abort
from bot import client, send
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

print(datetime.now(pytz.timezone("America/New_York")))

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
async def handle_hello():
    await send("bot-spam", "hello!")
    return "hi!", 200

@app.route('/whiteroom', methods=['POST'])
async def handle_whiteroom():
    body = request.json
    await send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"])
    await send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"])
    await send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"])
    await send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"])
    await send("bot-spam", ":white_large_square: You got whiteroomed  :white_large_square:", body["user"])
    return "Success", 200

@app.route('/rune', methods=['POST'])
async def handle_rune():
    body = request.json
    await send("bot-spam", "Rune is up :robot:", body["user"])
    return "Success", 200

@app.route('/someone_entered_map', methods=['POST'])
async def handle_someone_entered_map():
    body = request.json
    await send("bot-spam", "Someone entered your map  <:monkas:421119362225799178> <:monkas:421119362225799178> <:monkas:421119362225799178>", body["user"])
    return "Success", 200

@app.route('/started', methods=['POST'])
async def handle_started():
    body = request.json
    await send("bot-spam", f"Started his bot at :clock1: **{datetime.now(pytz.timezone('America/New_York')).strftime('%H:%M:%S')} EST** :clock1:", body["user"])
    return "Success", 200
"""
Auto add menber to Discord server with a token received from Discord API

and rick roll
"""

import json

import uvicorn
from aiohttp import ClientSession
from fastapi.responses import RedirectResponse

from app import CApp

app = CApp()
ipc = Client(secret_key="🐼")

with open("settings.json", "r", encoding="utf8") as f:
    settings = json.load(f)

CLIENT_ID = settings["CLIENT_ID"]
CLIENT_SECRET = settings["CLIENT_SECRET"]
DISCORD_TOKEN = settings["DISCORD_TOKEN"]
REDIRECT_URI = settings["REDIRECT_URI"]
API_VERSION = settings["API_VERSION"]

ENDPOINT = "https://discord.com/api/" + API_VERSION

@app.on_event("startup")
async def startup_event():
    """
    Run at start up
    """

    app.http_sess = ClientSession()

async def exchange_code(code):
    """
    Exchange code for access token
    """

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    async with app.http_sess.post(
        url = f'{ENDPOINT}/oauth2/token',
        data = data,
        headers = headers
    ) as resp:
        return await resp.json()

async def get_user(access_token):
    """
    Get user ID and name from access token
    """

    headers = {
        "Authorization" : f"Bearer {access_token}"
    }

    async with app.http_sess.post(
        url = f"{ENDPOINT}/oauth2/@me",
        headers = headers
    ) as resp:
        data = await resp.json()

    return (data["user"]['id'], f"{data['user']['username']}#{data['user']['discriminator']}")

async def add_to_guild(access_token, user_id, bot_token):
    """
    Add user to guild
    """

    data = {
        "access_token" : access_token
    }
    headers = {
        "Authorization" : f"Bot {bot_token}",
        'Content-Type': 'application/json'
    }

    async with app.http_sess.post(
        url = f"{ENDPOINT}/guilds/912563175919083571/members/{user_id}",
        data = data,
        headers = headers
    ) as resp:
        return resp.status

@app.get("/join")
async def api_join(code: str):
    """
    Add a member to the server
    """

    access_token = await exchange_code(code)["access_token"]
    user_id, user_name = await get_user(access_token)

    await add_to_guild(access_token, user_id, DISCORD_TOKEN)
    print(f"Added {user_name} to the server")

    return RedirectResponse(
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ",
        status_code = 302
    )

if __name__ == "__main__":
    uvicorn.run("main:app", port = 42069, reload = True)

@app.get("/bot-server-count")
async def bot_server_count():
    """
    Return bot server count
    """


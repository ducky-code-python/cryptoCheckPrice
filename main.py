import json
import requests
from discord.ext import commands
import discord
import discord.ext.commands
from discord.ext import tasks
from datetime import datetime


# defining key/request url
key = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEUSDT"
  

with open('config.json') as file:
    data = json.load(file)
    discord_token = str(data['apiIDs']['discord'])
    discordUserID = str(data['apiIDs']['discordUserID'])
    
intent = discord.Intents.all()
intent.members = True
intent.message_content = True
client =  commands.Bot(command_prefix= ".", intents=intent)

TOKEN = discord_token


@tasks.loop(seconds=20)
async def myLoop():
    global discordUserID
    data = requests.get(key)  
    data = data.json()
    price = float(data['price'])
    if price >= 0.08:
        user = await client.fetch_user(discordUserID)
        await user.send(f"Check DOGECOIN")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current price: {price} || Updated {current_time}")

@client.event
async def on_ready():
    global discordUserID
    myLoop.start()
    user = await client.fetch_user(discordUserID)
    await user.send(f"Started")

@client.command()
async def price(ctx):
    global discordUserID
    data = requests.get(key)  
    data = data.json()
    price = float(data['price'])
    user = await client.fetch_user(discordUserID)
    await user.send(f"{price}")

client.run(TOKEN)

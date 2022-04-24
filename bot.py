from http import client
import os
from dotenv import load_dotenv
import discord

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WHEATER_TOKEN = os.getenv('BOT_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return
    
    if user_message.lower() == "£help":
        await message.channel.send("hello")
        return

client.run(BOT_TOKEN)


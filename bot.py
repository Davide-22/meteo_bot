from http import client
import os
from dotenv import load_dotenv
import discord
import requests
import datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')

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
        await message.channel.send("£meteo CITY_NAME N\nReturn the forecast in CITY_NAME, N days after today.")
        return
    
    m = user_message.split()
    if m[0] == "£meteo":
        day = 1
        date = "Tomorrow"
        if len(m) == 1:
            city = "roma"
        elif len(m) == 2:
            city = m[1]
        elif len(m) == 3:
            try:
                city = m[1]
                print(f"m: {m}")
                day = int(m[2])
                assert day <= 7 and day >= 0
                date = datetime.datetime.now()
                date = date + datetime.timedelta(days=day)
                date = date.strftime("%d %B %Y")
            except Exception as e:
                print(e)
                await message.channel.send("Type £help for the syntax")
                return
        else:
            await message.channel.send("Scrivi £help per la sintassi")
            return
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_TOKEN}"
        weather = requests.get(url).json()

        if weather == []:
            await message.channel.send("Unknown city name")
            return
            
        lat = weather[0]['lat']
        lon = weather[0]['lon']
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=hourly,minutely&appid={WEATHER_TOKEN}"
        weather = requests.get(url).json()
        temp = weather["daily"][day]["temp"]["day"]
        min = weather["daily"][day]["temp"]["min"]
        max = weather["daily"][day]["temp"]["max"]
        desc = weather["daily"][day]["weather"][0]["description"]
        msg = f"{city.capitalize()}\n{date}: {temp}°\nMin: {min}° Max: {max}°\n{desc.capitalize()}"
        await message.channel.send(msg)
        return
client.run(BOT_TOKEN)

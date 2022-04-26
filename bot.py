#!/bin/python

from http import client
import os
from traceback import print_tb
from xml.dom import SYNTAX_ERR
from dotenv import load_dotenv
import discord
import requests
import datetime

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
SYNTAX_ERR = "Type £help for the syntax"
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
        await message.channel.send("£meteo CITY_NAME N\nReturn the forecast in CITY_NAME, N days after today (0 <= N <= 7).")
        return
    
    m = user_message.split()
    if m[0] == "£meteo":
        day = 1
        city = ""
        date = "Tomorrow"
        if len(m) == 1:
            city = "roma"
        elif len(m) == 2:
            city = m[1]
        else:
            try:
                day = int(m[len(m)-1])
                print(m)
                for i in range(1,len(m)-1):
                    print(m[i])
                    city += m[i]
                    if i != len(m)-2:
                        city += " "
                assert day <= 7 and day >= 0
                date = datetime.datetime.now()
                date = date + datetime.timedelta(days=day)
                date = date.strftime("%B %d %Y")
            except ValueError as e:
                for i in range(1,len(m)):
                    city += m[i]
                    if i != len(m)-1:
                        city += " "
            except AssertionError as e:
                print(e)
                await message.channel.send(SYNTAX_ERR)
                return
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_TOKEN}"
        weather = requests.get(url).json()
        print(url)
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
        msg = f"{city.title()}\n{date}: {temp}°\nMin: {min}° Max: {max}°\n{desc.capitalize()}"
        await message.channel.send(msg)
        return
        
client.run(BOT_TOKEN)

#!/bin/python

from http import client
import os
from dotenv import load_dotenv
import discord
import requests
import datetime

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_TOKEN = os.getenv('WEATHER_TOKEN')
SYNT_ERR = "Type £help for the syntax"
CMD1 = "meteo"
CMD2 = "today"
CMD3 = "poll"

client = discord.Client()

def getMeteo(url):
    weather = requests.get(url).json()
    return weather

def getLatLon(city):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_TOKEN}"
    weather = getMeteo(url)
    print(weather)
    if weather == []:
        return -200,-200
    lat = weather[0]['lat']
    lon = weather[0]['lon']
    return lat, lon

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
        with open("help.txt") as f:
            msg = f.read().format(cmd1 = CMD1,cmd2 = CMD2,cmd3 = CMD3)
        await message.channel.send(msg)
        return
    
    m = user_message.split()

    #Daily forecast
    if m[0] == f"£{CMD1}":
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
                if day == 0:
                    date = "Today"
                elif day != 1:
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
                await message.channel.send(SYNT_ERR)
                return
        lat, lon = getLatLon(city)
        if lat == -200:
            await message.channel.send("Unknown city name")
            return
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=hourly,minutely&appid={WEATHER_TOKEN}"
        weather = getMeteo(url)
        temp = weather["daily"][day]["temp"]["day"]
        min = weather["daily"][day]["temp"]["min"]
        max = weather["daily"][day]["temp"]["max"]
        max = weather["daily"][day]["temp"]["max"]
        night = weather["daily"][day]["temp"]["night"]
        feels_like = weather["daily"][day]["feels_like"]["day"]
        desc = weather["daily"][day]["weather"][0]["description"]
        msg = f"{city.title()}\n{date}\nDay: {temp}° Night:{night}°\nMin: {min}° Max: {max}°\nFeels like: {feels_like}°\n{desc.capitalize()}"
        await message.channel.send(msg)
        return

    #Hourly forecast
    if m[0] == f"£{CMD2}":
        limit = 15
        city = ""
        if len(m) == 1:
            city = "roma"
        elif len(m) == 2:
            city = m[1]
        else:
            try:
                limit = int(m[len(m)-1])
                for i in range(1,len(m)-1):
                    print(m[i])
                    city += m[i]
                    if i != len(m)-2:
                        city += " "
                assert limit <= 47 and limit >= 0
            except ValueError as e:
                for i in range(1,len(m)):
                    city += m[i]
                    if i != len(m)-1:
                        city += " "
            except AssertionError as e:
                print(e)
                await message.channel.send(SYNT_ERR)
                return
        lat, lon = getLatLon(city)
        if lat == -200:
            await message.channel.send("Unknown city name")
            return
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&exclude=daily,minutely&appid={WEATHER_TOKEN}"
        weather = getMeteo(url)
        msg = f"{city.title()}\n"
        for i in range(limit+1):
            temp = weather["hourly"][i]["temp"]
            feels_like = weather["hourly"][i]["feels_like"]
            desc = weather["hourly"][i]["weather"][0]["description"]
            date = datetime.datetime.fromtimestamp(weather["hourly"][i]["dt"])
            msg += f"{date}: {temp}°\nFeels like: {feels_like}\n{desc.capitalize()}\n\n"
        await message.channel.send(msg)
        return
    
    #Air pollution
    if m[0] == f"£{CMD3}":
        poll_array = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]
        city = ""
        if len(m) < 2:
            await message.channel.send(SYNT_ERR)
            return
        for i in range(1,len(m)):
                    print(m[i])
                    city += m[i]
                    if i != len(m)-2:
                        city += " "
        lat,lon = getLatLon(city)
        if lat == -200:
            await message.channel.send("Unknown city name")
            return
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_TOKEN}"
        poll = getMeteo(url)
        aq = poll_array[int(poll["list"][0]["main"]["aqi"])-1]
        msg = f"{city.title()}\nAir quality: {aq}"
        await message.channel.send(msg)
        return
        
client.run(BOT_TOKEN)

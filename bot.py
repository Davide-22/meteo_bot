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
        await message.channel.send("hello")
        return
    
    m = user_message.split()
    if m[0] == "£meteo":
        day = 1
        if len(m) == 1:
            city = "roma"
        elif len(m) == 2:
            city = m[1]
        elif len(m) == 3:
            day = int(m[2])
        else:
            await message.channel.send("error")
            return
        url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={WEATHER_TOKEN}"
        weather = requests.get(url).json()
        lat = weather[0]['lat']
        lon = weather[0]['lon']
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&lang=it&exclude=hourly,minutely&appid={WEATHER_TOKEN}"
        weather = requests.get(url).json()
        temp = weather["daily"][day]["temp"]["day"]
        min = weather["daily"][day]["temp"]["min"]
        max = weather["daily"][day]["temp"]["max"]
        #w = weather["daily"][day]["weather"][0]["main"]
        desc = weather["daily"][day]["weather"][0]["description"]
        msg = f"{city.capitalize()}\nDomani: {temp}°\nMinima: {min}° Massima: {max}°\n{desc.capitalize()}"
        await message.channel.send(msg)
        return
client.run(BOT_TOKEN)

[{"dt":1650909600,"sunrise":1650886439,"sunset":1650934434,"moonrise":1650877320,"moonset":1650916680,"moon_phase":0.83,"temp":{"day":291.06,"min":287.67,"max":295.34,"night":287.67,"eve":291.04,"morn":290.62},"feels_like":{"day":291.02,"night":287.24,"eve":290.9,"morn":290.82},"pressure":1020,"humidity":81,"dew_point":287.75,"wind_speed":5.93,"wind_deg":27,"wind_gust":13.32,"weather":[{"id":502,"main":"Rain","description":"heavy intensity rain","icon":"10d"}],"clouds":100,"pop":1,"rain":11.46,"uvi":2.05},{"dt":1650996000,"sunrise":1650972775,"sunset":1651020880,"moonrise":1650965640,"moonset":1651006920,"moon_phase":0.86,"temp":{"day":292.09,"min":282.91,"max":293.82,"night":284.51,"eve":290.98,"morn":282.91},"feels_like":{"day":291.29,"night":283.66,"eve":290.54,"morn":280.89},"pressure":1027,"humidity":48,"dew_point":280.83,"wind_speed":5.34,"wind_deg":51,"wind_gust":12.3,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":33,"pop":0,"uvi":9.52},{"dt":1651082400,"sunrise":1651059111,"sunset":1651107326,"moonrise":1651053840,"moonset":1651097040,"moon_phase":0.9,"temp":{"day":291.81,"min":280.36,"max":294.16,"night":286.19,"eve":291.83,"morn":280.36},"feels_like":{"day":290.93,"night":285.25,"eve":291.35,"morn":278.47},"pressure":1024,"humidity":46,"dew_point":279.94,"wind_speed":3.44,"wind_deg":94,"wind_gust":8.75,"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01d"}],"clouds":0,"pop":0,"uvi":10.17},{"dt":1651168800,"sunrise":1651145448,"sunset":1651193772,"moonrise":1651141920,"moonset":1651187040,"moon_phase":0.93,"temp":{"day":296.26,"min":282.97,"max":298.98,"night":291.21,"eve":295.62,"morn":283.12},"feels_like":{"day":296.01,"night":291.03,"eve":295.85,"morn":281.93},"pressure":1016,"humidity":53,"dew_point":286.22,"wind_speed":4.15,"wind_deg":177,"wind_gust":6.56,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":91,"pop":0,"uvi":8.9},{"dt":1651255200,"sunrise":1651231787,"sunset":1651280219,"moonrise":1651229940,"moonset":1651276980,"moon_phase":0.96,"temp":{"day":300.15,"min":288.74,"max":302.03,"night":295.84,"eve":298.01,"morn":288.74},"feels_like":{"day":300.95,"night":295.89,"eve":298.46,"morn":288.91},"pressure":1012,"humidity":56,"dew_point":290.71,"wind_speed":5.32,"wind_deg":184,"wind_gust":12.99,"weather":[{"id":802,"main":"Clouds","description":"scattered clouds","icon":"03d"}],"clouds":26,"pop":0.15,"uvi":9},{"dt":1651341600,"sunrise":1651318126,"sunset":1651366665,"moonrise":1651318020,"moonset":1651366980,"moon_phase":0,"temp":{"day":299.77,"min":290.84,"max":299.77,"night":293.42,"eve":296.73,"morn":290.84},"feels_like":{"day":299.77,"night":293.88,"eve":297.34,"morn":291.12},"pressure":1010,"humidity":61,"dew_point":291.77,"wind_speed":5.67,"wind_deg":194,"wind_gust":13.4,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":89,"pop":0.79,"rain":2.25,"uvi":9},{"dt":1651428000,"sunrise":1651404467,"sunset":1651453111,"moonrise":1651406220,"moonset":1651456920,"moon_phase":0.03,"temp":{"day":300.42,"min":290.7,"max":300.42,"night":294.22,"eve":298.52,"morn":290.88},"feels_like":{"day":301.83,"night":294.55,"eve":299.1,"morn":291.27},"pressure":1012,"humidity":63,"dew_point":292.75,"wind_speed":6.66,"wind_deg":176,"wind_gust":14.17,"weather":[{"id":500,"main":"Rain","description":"light rain","icon":"10d"}],"clouds":38,"pop":0.71,"rain":3.29,"uvi":9},{"dt":1651514400,"sunrise":1651490808,"sunset":1651539558,"moonrise":1651494660,"moonset":1651546860,"moon_phase":0.06,"temp":{"day":301.27,"min":292.09,"max":302.86,"night":297.23,"eve":298.67,"morn":292.09},"feels_like":{"day":302.44,"night":297.44,"eve":299.11,"morn":292.52},"pressure":1012,"humidity":57,"dew_point":291.96,"wind_speed":5.38,"wind_deg":180,"wind_gust":14.58,"weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],"clouds":97,"pop":0.8,"uvi":9}]
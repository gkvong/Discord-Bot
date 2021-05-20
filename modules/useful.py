"""This module contains useful commands"""
import discord
from discord.ext import commands
import os
import sys
import random
import string
import asyncio
import json
import requests
from datetime import datetime

from translate import Translator
import wikipedia

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('weatherapp_id')

class Useful(commands.Cog, name = "Useful Commands"):
    """Commands that are actually useful Pog."""

    # Weather OpenWeatherMap
    @commands.command()
    async def weather(self, ctx, *city):
        """ Get the current weather in a city.
            Leave city empty to get the weather in Sydney.
            For most accurate results, include the country code like this:
            '$weather london,uk'."""
        if len(city) == 0:
            city = "sydney"
        else:
            city = " ".join(city)
            
        print(ctx.author.name + " | Command: Weather " + city)
            
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
            data = requests.get(url).json()

            city = data['name'] 
            country = data['sys']['country']
            weather_icon = data['weather'][0]['icon']
            weather_desc = data['weather'][0]['description']
            temp = round(data['main']['temp'])
            clouds = str(round(data['clouds']['all']))
            wind_speed = round(data['wind']['speed'])
            humidity = data['main']['humidity']
            date = datetime.fromtimestamp(data['dt']-39600 +data['timezone'])
            
            if temp >= 30:
                embed = discord.Embed(type="rich", colour= discord.Colour.red())
            elif 25 <= temp < 30:
                embed = discord.Embed(type="rich", colour= discord.Colour.orange())
            elif 20 <= temp < 25:
                embed = discord.Embed(type="rich", colour= discord.Colour.blurple())
            elif 10 < temp < 20:
                embed = discord.Embed(type="rich", colour= discord.Colour.dark_blue())
            else:
                embed = discord.Embed(type="rich", colour= discord.Colour.blue())
                
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_icon}@2x.png")
            embed.set_author(name=f"{city}, {country}")
            embed.add_field(name=f"{str(temp)}°C", value=f"{weather_desc}", inline=False)
            embed.add_field(name="\u200b", value=f"Cloudiness: {clouds}% \n Wind: {wind_speed} m/s \n Humidity: {humidity}%", inline=False)
            embed.set_footer(text=date.strftime('%I:%M %p, %b %d'))

            await ctx.send(embed=embed)
        except:
            await ctx.send(f"No weather data found for '{city}'.")
        await asyncio.sleep(1)

    # Forecast OpenWeatherMap
    @commands.command()
    async def forecast(self,ctx):
        """Get the 7-day Sydney weather forecast.
            There is a 10 second timeout for this command."""
        print(ctx.author.name + " | Command: Forecast")
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat=-33.8679&lon=151.2073&exclude=current,hourly,minutely,hourly,alerts&units=metric&appid={API_KEY}"
        forecast = requests.get(url).json()
        
        embed = discord.Embed(type="rich", colour=discord.Colour.dark_theme())
        embed.set_author(name="Forecast for Sydney, AU")
        await ctx.send(embed=embed)

        i = 0
        while i <= 7:
            dayData = forecast['daily'][i]
            weather_icon = dayData['weather'][0]['icon']
            weather_desc = dayData['weather'][0]['description']
            temp_min = round(dayData['temp']['min'])
            temp_max = round(dayData['temp']['max'])
            temp = round(dayData['temp']['day'])
            date = datetime.fromtimestamp(dayData['dt']-39600 +forecast['timezone_offset'])

            if temp >= 30:
                embed = discord.Embed(type="rich", colour= discord.Colour.red())
            elif 25 <= temp < 30:
                embed = discord.Embed(type="rich", colour= discord.Colour.orange())
            elif 20 <= temp < 25:
                embed = discord.Embed(type="rich", colour= discord.Colour.blurple())
            elif 10 < temp < 20:
                embed = discord.Embed(type="rich", colour= discord.Colour.dark_blue())
            else:
                embed = discord.Embed(type="rich", colour= discord.Colour.blue())
            
            embed.add_field(name=f"{str(temp_max)}° | {str(temp_min)}°", value=f"{weather_desc}")
            embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_icon}@2x.png")
            embed.set_footer(text=date.strftime('%A, %b %d'))
            await ctx.send(embed=embed)
            i += 1
            
        await asyncio.sleep(10)
        
    # Define Google Dictionary
    @commands.command()
    async def define(self, ctx, *, query):
         """Search for a definition from Google Dictionary."""
         print(ctx.author.name + " | Command: Define") 
         try:
             url = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
             rawData = requests.get(url + query).json()
             
             word = rawData[0]['word']
             
             meanings = rawData[0]['meanings']
             
             embed = discord.Embed(type="rich")
             embed.set_author(name = f"Dictionary: {word}")

             i = 0
             while i < len(meanings):
                 title = meanings[i]['partOfSpeech']
                 definition = meanings[i]['definitions'][0]['definition']
                 example = meanings[i]['definitions'][0]['example']
                 embed.add_field(name=title, value=definition + f'\n "    {example}"', inline=False)
                 i +=1
             
             await ctx.send(embed=embed)
         except:
             await ctx.send(ctx.author.mention + " No definition found for '" + query + "'.")
             

    # Translate
    @commands.command()
    async def translate(self, ctx, code1, code2, text):
            """Translate a message.
               Use this command like: '$translate en ja hello' to translate 'hello' from English to Japanese. See
               https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
               for language codes."""
            print(ctx.author.name + " | Command: Translate") 
            query = ctx.message.content
            query = query.split()

            fromlang = query[1]
            tolang = query[2]

            message = ""
            for x in query[3:]:
                    message += x 
                    message += " "

            translator = Translator(to_lang=tolang, from_lang=fromlang)
            translation = translator.translate(message)

            output = message
            output += " ("
            output += fromlang
            output += " → "
            output += tolang
            output += "): "
            output += "`" + translation + "`"

            await ctx.message.channel.send(output)


    # Wikipedia
    @commands.command()
    async def wiki(self, ctx, *, query):
            """Get the first few sentences of a Wikipedia page."""
            queryComputeMessage = await ctx.send("**Query:** " + query + "\n**Searching Wikipedia...** :hourglass:")
            print(ctx.author.name + " | Command: Wiki") 
            try:
                query = ctx.message.content
                query = query.replace('$wiki', '')

                summary = wikipedia.summary(query, auto_suggest=True, sentences=2)
                page = wikipedia.page(query, auto_suggest=True)

                title = "Wikipedia: "
                title += page.title
                URL = page.url
                
                embed = discord.Embed(type="rich")
                embed.set_author(name=title)
                embed.add_field(name="Summary", value=summary, inline=False)
                embed.set_image(url=page.images[0])
                embed.add_field(name="Read More", value=URL, inline=False)
                
                await ctx.message.channel.send(embed=embed)
                await queryComputeMessage.edit(content = "**Query:** " + query + "\n" + ctx.author.mention + " Done!")
                
            except(wikipedia.exceptions.DisambiguationError):
                await queryComputeMessage.edit(content = "**Query:** " + query + "\n" + ctx.author.mention + " **Disambiguation error:** Please try a more specific query.")
            except(wikipedia.exceptions.PageError):
                 await queryComputeMessage.edit(content = "**Query:** " + query + "\n" + ctx.author.mention + " **Page error:** '" + query + "' Does not match any pages. Try another query!")
 
def setup(bot):
    bot.add_cog(Useful(bot))
    print("Useful Commands module loaded.")

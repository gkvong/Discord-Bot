#!/usr/bin/python

import discord
from discord.ext import commands
import os
import asyncio

import modules.useful
import modules.trivia
import modules.minesweeper

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Configure intents
intents = discord.Intents.default()

# Configure help command 
helpcommand = commands.DefaultHelpCommand(no_category="Bot Commands")

# Discord bot session
bot = commands.Bot(command_prefix = '$', intents=intents, help_command=helpcommand)

# Bot modules
bot.load_extension('modules.useful')
bot.load_extension('modules.trivia')
bot.load_extension('modules.minesweeper')

# Discord connection confirmation
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord.")
    print("----------------------------------------")

# Ping
@bot.command(aliases=["PING"])
async def ping(ctx):
    """ Get the latency of the bot. """
    print(str(ctx.author) + " | Command: Ping")
    await ctx.send(f"Ping: {round(bot.latency*1000)} ms")

#On message event triggers
@bot.event
async def on_message(message):
    
    # Anti recursion
    if message.author == bot.user:
        return
    
    msg = message.content

    # Trivia answer listener
    if message.channel.id in bot.trivia_games:
            await bot.trivia_games[message.channel.id].process_message(message)

    await bot.process_commands(message)

bot.run(os.getenv('TOKEN'))

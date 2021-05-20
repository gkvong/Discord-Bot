"""This module contains the trivia functionality"""
import discord
from discord.ext import commands
import requests
import json
import random
import html
import asyncio

incorrect_users = []
    
async def penalty(msg):
    """"Adds a 5s penalty to a user for a wrong answer"""
    incorrect_users.append(msg.author.id)
    penaltymsg = await msg.channel.send(msg.author.mention + " +5s penalty.")
    await penaltymsg.delete(delay=5)
    await asyncio.sleep(5)
    del incorrect_users[0]
    
def multiplechoice(letters,choices):
    i = 0
    s = ""
    while i < len(choices):
        s += "**" + letters[i] + f":** `{html.unescape(choices[i])}`\n"
        i += 1
    return html.unescape(s)

class TriviaGame():
    """"Trivia"""
    def __init__(self, ctx, *, bot):
        """"Fetches trivia data from API and sends initial embed."""
        self.bot = bot
        self.ctx = ctx
        self.channel = ctx.message.channel
        self.message = None

        urls = ["https://beta-trivia.bongo.best", "https://opentdb.com/api.php?amount=1"]
        url = random.choice(urls)
        triviaData = requests.get(url).json()
        if url == "https://beta-trivia.bongo.best":
            trivia = triviaData[0]
        else:
            trivia = triviaData['results'][0]

        self.category = trivia['category']
        if self.category == None:
            self.category = 'General Knowledge'
        
        self.question = html.unescape(trivia['question'])
        self.correct_answer = html.unescape(trivia['correct_answer'])
        incorrect_answers = trivia['incorrect_answers']

        self.choices = incorrect_answers + [self.correct_answer]
        self.choices = [x.strip() for x in self.choices]
        
        for x in self.choices:
            if "https://t.co/" in x:
                return(self.__init__(ctx = self.ctx, bot = self.bot))
        
        random.shuffle(self.choices)
        
        self.letters = ["A", "B", "C", "D"]
        self.letters_lower = ["a", "b", "c", "d"]
        self.options = multiplechoice(self.letters,self.choices)

        self.embed = discord.Embed(timestamp=ctx.message.created_at)
        self.embed.description = f"{self.category}\n\u200b"
        self.embed.set_footer(text="Initiated by {}".format(str(ctx.message.author)))
        self.embed.add_field(name=f"**{self.question}**", value=f"{self.options}\n\u200b",inline=False)

    async def start(self):
        """Starts the game"""
        self.message = await self.channel.send(embed=self.embed)

    async def process_message(self, msg):
        """Processes the message"""       
        if msg.content.lower() in self.letters_lower[self.choices.index(self.correct_answer.strip())]:
            if msg.author.id not in incorrect_users:
                embed = self.embed
                embed.clear_fields()
                    
                edit = self.options.replace(f"`{self.correct_answer}`",f"**{self.correct_answer}**")

                embed.add_field(name=f"**{self.question}**", value=f"{edit}\n{msg.author.mention} got the answer right! It was **{self.correct_answer}**.",inline=False)
                embed.colour = 0x4BB543

                await msg.delete()
                del self.bot.trivia_games[self.channel.id]
                await self.message.edit(embed=embed)
            else:
                await msg.delete()
                await penalty(msg)
            
        elif msg.content.lower() in [letter for letter in self.letters_lower if letter != self.letters_lower[self.choices.index(self.correct_answer.strip())]]:
            await msg.delete()
            await penalty(msg)
            
class Trivia(commands.Cog):
    """Trivia"""
    def __init__(self,bot):
        self.bot = bot
        self.bot.trivia_games = {}
        
    @commands.command(pass_context=True)
    async def trivia(self, ctx):
        """Test your knowledge with random trivia!"""
        print(ctx.author.name + " | Command: Trivia")
        self.bot.trivia_games[ctx.message.channel.id] = TriviaGame(ctx, bot=self.bot)
        await self.bot.trivia_games[ctx.message.channel.id].start()

def setup(bot):
    bot.add_cog(Trivia(bot))
    print("Trivia module loaded.")

import json
import discord
import random as r
from discord.ext import commands
from cogs.assets.custombot import CustomBot


class Animals(commands.Cog):
    """Class description"""
    def __init__(self, bot: CustomBot): self.bot = bot
    
    @commands.command(aliases= ["purr", "kitty"])
    @commands.cooldown(3, 3)
    async def cat(self, ctx):
        """Its a kitty! 🐱"""
        await ctx.trigger_typing()
        async with self.bot.requester.get("http://aws.random.cat/meow") as resp:
            url= json.loads(await resp.read())["file"]
        
        embed= discord.Embed(title= "Meow! :heart_eyes_cat:", color= r.randint(0, 0xFFFFFF))
        embed.set_image(url= url)
        
        await ctx.send(embed= embed)


    @commands.command(aliases= ["foxx", "floof"])
    @commands.cooldown(3, 3)
    async def fox(self, ctx):
        """Foxxxxxx! 🦊"""
        await ctx.trigger_typing()
        async with self.bot.requester.get("https://randomfox.ca/floof/") as resp:
            data= json.loads(await resp.read())
        
        embed= discord.Embed(title= "No clue what the fox says 🦊", color= r.randint(0, 0xFFFFFF))
        embed.set_image(url= data["image"])
        
        await ctx.send(embed= embed)


    @commands.command(aliases= ["quack", "ducc"])
    @commands.cooldown(3, 3)
    async def duck(self, ctx):
        """Quack quack! 🦆"""
        await ctx.trigger_typing()
        async with self.bot.requester.get("https://random-d.uk/api/random") as resp:
            data= json.loads(await resp.read())
        
        embed= discord.Embed(title= "Quack quack! 🦆", color= r.randint(0, 0xFFFFFF))
        embed.set_image(url= data["url"])
        
        await ctx.send(embed= embed)


    @commands.command()
    @commands.cooldown(3, 3)
    async def panda(self, ctx):
        """Look ma! Its a panda! 🐼"""
        await ctx.trigger_typing() # I should get a less dodgy api but oh well
        url = r.choice(["https://some-random-api.ml/pandaimg", "https://some-random-api.ml/redpandaimg"])
        async with self.bot.requester.get(url) as resp:
            data= json.loads(await resp.read())
        
        embed= discord.Embed(title= "Look ma! Its a panda! 🐼", color= r.randint(0, 0xFFFFFF))
        embed.set_image(url= data["link"])
        
        await ctx.send(embed= embed)


def setup(bot): bot.add_cog(Animals(bot))
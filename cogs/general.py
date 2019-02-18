import time
import discord
import random as r
from discord.ext import commands

class General:
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def example(self, ctx):
        await ctx.send(embed=discord.Embed(
            title= 'yeet',
            description= 'no u'
        ))


    @commands.command()
    async def info(self, ctx):
        await ctx.send(embed=discord.Embed(color= r.randint(0, 0xFFFFFF), description=
            f"Yeet yeet my dudes: {str(self.bot.latency)}"
        ))


    @commands.command()
    async def suggest(self, ctx, suggestion):
        await self.bot.send('yeet yeet', 'no u')
    
    @commands.command()
    @commands.cooldown(1, 60)
    async def time(self, ctx):
        await self.bot.send('yayeet', f'the time is {time.time()}')


def setup(bot): bot.add_cog(General(bot))
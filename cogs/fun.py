import discord
from discord.ext import commands

class Fun:
    def __init__(self, bot): self.bot = bot
    
    @commands.command()
    async def example(self, ctx):
        pass


def setup(bot): bot.add_cog(Fun(bot))
import discord
from discord.ext import commands

class Currency:
    def __init__(self, bot): self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 86400)
    async def daily(self, ctx):
        """Yeet yeet, free money!"""
        await self.bot.send('yayeet', 'heres ur money! :moneybag:')


def setup(bot): bot.add_cog(Currency(bot))
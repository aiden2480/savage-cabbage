import discord
from discord.ext import commands

class Template:
    def __init__(self, bot): self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 86400)
    async def daily(self, ctx):
        await self.bot.send('yayeet', 'heres ur money! :moneybag:')


def setup(bot): bot.add_cog(Template(bot))
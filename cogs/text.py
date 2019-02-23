import discord
from setup import emojis
from discord.ext import commands

class Text:
    def __init__(self, bot): self.bot = bot
    
    @commands.command()
    @commands.cooldown(1, 2)
    async def partyparrot(self, ctx, text= None):
        """Send kewl messages with the partyparrot emoji"""
        
        if text is None: await self.bot.send("", emojis.partyparrot.join(text.split()))
        else: await self.bot.send("", f"What do you want me to {emojis.partyparrot}")


def setup(bot): bot.add_cog(Text(bot))
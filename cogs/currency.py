import os
import discord
import json_store_client
from setup import emojis
# from cogs.assets import database
from discord.ext import commands

class Currency(commands.Cog):
    """Creating a currency system soon!"""
    def __init__(self, bot): self.bot, self.db = bot, json_store_client.Client(os.getenv("DATABASE_URL"))

    @commands.command()
    @commands.cooldown(1, 86400)
    async def daily(self, ctx):
        """Yeet yeet, free money!"""
        async with ctx.typing():
            self.db.store(f"users/{ctx.author.id}/money/wallet", int(self.db.get(f"users/{ctx.author.id}/money/wallet"))+100)
            await self.bot.send("Here's ya money :moneybag:", "100 coins added to ya wallet :dollar:")
    

    @commands.command()
    @commands.cooldown(2, 3)
    async def bal(self, ctx):
        await ctx.trigger_typing()
        bal = self.db.get(f"users/{ctx.author.id}/money/wallet")
        await ctx.send(f"Your balance is {emojis.coin}**{bal}**")
    



def setup(bot: commands.Bot):
    return # Still working on this
    bot.add_cog(Currency(bot))
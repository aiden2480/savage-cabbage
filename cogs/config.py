import os
import discord
import random as r
import json_store_client
from setup import emojis
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot): self.bot, self.db = bot, json_store_client.Client(os.getenv("DATABASE_URL"))

    @commands.guild_only()
    @commands.cooldown(3, 5)
    @commands.command(name= "prefix")
    async def _prefix(self, ctx, *, prefix= None):
        """Change the bot prefix for this server!"""

        if prefix is None:
            embed= discord.Embed(description= f"Your server prefix is `{self.bot.serverprefixes[str(ctx.guild.id)]}`", color= r.randint(0, 0xFFFFFF))
            embed.set_footer(text= f"Use '{ctx.prefix}prefix <prefix>' to set the prefix!")
            await ctx.send(embed= embed)
        elif ctx.author.guild_permissions.manage_guild:
            if len(prefix) > 5: await ctx.send(f"Your prefix cannot be longer than 5 characters {emojis.thinkok}")
            else:
                await ctx.trigger_typing()
                self.db.store(f"server-prefixes/{ctx.guild.id}", {prefix})
                await ctx.send(f"👍 Success! Your server prefix is now `{prefix}`")
        else: await ctx.send("You need `manage server` perms to change the prefix!")
            
    @commands.command()
    @commands.guild_only()
    async def blah(self, ctx):
        await ctx.send("no u")


def setup(bot): bot.add_cog(Config(bot))
import discord
import random as r
from discord.ext import commands

class Admin:
    def __init__(self, bot):
        self.bot = bot
    
    def admin_check(self, id):
        if id in [
            272967064531238912, # Me
        ]: return True
        return False

    @commands.command()
    async def unloadcog(self, ctx, cog):
        if not self.admin_check(ctx.author.id): return await ctx.send("Admin only command, sorry ❎")
        self.bot.unload_extension(f"cogs.{cog}")


    @commands.command()
    async def loadcog(self, ctx, cog):
        if not self.admin_check(ctx.author.id): return await ctx.send("Admin only command, sorry ❎")
        self.bot.load_extension(f"cogs.{cog}")

    @commands.command()
    async def reloadcog(self, ctx, cog):
        if not self.admin_check(ctx.author.id): return await ctx.send("Admin only command, sorry ❎")
        
        embed= discord.Embed(
            description= f"Unloading cog {cog} ↪",
            color= r.randint(0, 0xFFFFFF))
        msg= await ctx.send(embed= embed)

        self.bot.unload_extension(f"cogs.{cog}")

        embed.description= f"Loading cog {cog} ↩"
        await msg.edit(embed= embed)

        self.bot.load_extension(f"cogs.{cog}")

        embed.description= f"Cog {cog} reloaded! ✅"
        await msg.edit(embed= embed)


def setup(bot): bot.add_cog(Admin(bot))
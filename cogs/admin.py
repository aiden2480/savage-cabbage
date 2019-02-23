import inspect
import discord
import random as r
from discord.ext import commands

class Admin:
    def __init__(self, bot):
        self.bot = bot


    @commands.is_owner()
    @commands.command(hidden= True)
    async def unloadcog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(embed= discord.Embed(description= f"Cog **{cog}** unloaded ✅", color= r.randint(0, 0xFFFFFF)))
        except Exception as e:
            await ctx.send(f"**Error:**\n```py\n{e}```")
            raise e


    @commands.is_owner()
    @commands.command(hidden= True)
    async def loadcog(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed= discord.Embed(description= f"Cog **{cog}** loaded ✅", color= r.randint(0, 0xFFFFFF)))
        except Exception as e:
            await ctx.send(f"**Error:**\n```py\n{e}```")
            raise e


    @commands.is_owner()
    @commands.command(hidden= True)
    async def reloadcog(self, ctx, cog):        
        embed= discord.Embed(
            description= f"Unloading cog **{cog}** :arrows_counterclockwise:",
            color= r.randint(0, 0xFFFFFF))
        msg= await ctx.send(embed= embed)
        self.bot.unload_extension(f"cogs.{cog}")

        try:
            embed.description= f"Loading cog **{cog}** :arrows_clockwise:"
            await msg.edit(embed= embed)
            self.bot.load_extension(f"cogs.{cog}")

            embed.description= f"Cog **{cog}** reloaded! ✅"
            await msg.edit(embed= embed)
        except Exception as e:
            embed.description= f"**Error:**\n```py\n{e}```"
            await msg.edit(embed= embed)


    @commands.is_owner()
    @commands.command(hidden= True)
    async def source(self, ctx, command):
        """Get the command source"""
        cmd = self.bot.get_command(command)
        if cmd is None: return await self.bot.send("", "Could not find that command :x:")
        await ctx.send(f"Here ya go\n```py\n{getsource(cmd.callback)}```")

def setup(bot): bot.add_cog(Admin(bot))
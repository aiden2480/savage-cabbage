import time
import inspect
import discord
import random as r
from inspect import getsource
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot): self.bot = bot


    # Loading and unloading cogs
    @commands.is_owner()
    @commands.command(hidden= True, aliases= ["load"])
    async def loadcog(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(embed= discord.Embed(description= f"Cog **{cog}** loaded ✅", color= r.randint(0, 0xFFFFFF)))
        except Exception as e:
            await ctx.send(f"**Error:**\n```py\n{e}```")
            raise e


    @commands.is_owner()
    @commands.command(hidden= True, aliases= ["unload"])
    async def unloadcog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(embed= discord.Embed(description= f"Cog **{cog}** unloaded ✅", color= r.randint(0, 0xFFFFFF)))
        except Exception as e:
            await ctx.send(f"**Error:**\n```py\n{e}```")
            raise e

    
    @commands.is_owner()
    @commands.command(hidden= True)
    async def reload(self, ctx, cog= None):
        """Reload a cog (or the entire bot)... in style!"""
        if cog != None: # Reload cog
            embed= discord.Embed(
                description= f"Unloading cog **{cog}** 🔄",
                color= r.randint(0, 0xFFFFFF))
            msg= await ctx.send(embed= embed)
            self.bot.unload_extension(f"cogs.{cog}")

            try:
                embed.description= f"Loading cog **{cog}** 🔁"
                await msg.edit(embed= embed)
                self.bot.load_extension(f"cogs.{cog}")

                embed.description= f"Cog **{cog}** reloaded! ✅"
                await msg.edit(embed= embed)
            except Exception as e:
                embed.description= f"**Error:**\n```py\n{e}```"
                await msg.edit(embed= embed)
            return

        # # # # # # # # # # # # # Reload bot # # # # # # # # # # # # # #

        def update_embed(embed):
            """Let's hope that the globaling works -_-"""
            
            embed.clear_fields()
            embed.add_field(name= "Previous cogs", value= "\n".join(prev_cogs) or "None")
            embed.add_field(name= "Reloaded cogs", value= "\n".join(reloaded_cogs) or "None")
            return embed


        try:
            embed= discord.Embed(description= "*really* reload the entire bot? (15 sec timeout)", color= r.randint(0, 0xFFFFFF))
            msg = await ctx.send(embed= embed)
            def check(reaction, user): return user == ctx.author and str(reaction.emoji) == "👍"
            await msg.add_reaction("👍")
            await self.bot.wait_for("reaction_add", timeout= 15.0, check= check)
        except:
            embed.description= "Timed out"
            await msg.edit(embed= embed)
            return await msg.remove_reaction("👍", self.bot.user)

        prev_cogs, reloaded_cogs = sorted(set([cog.lower() for cog in list(self.bot.cogs)])), []
        embed = discord.Embed(title= "Reloading all cogs", description= "Starting ⏳", color= r.randint(0, 0xFFFFFF))
        embed = update_embed(embed)
        await msg.edit(embed= embed)
        _ = time.time()

        for cog in sorted(set([cog.lower() for cog in list(self.bot.cogs)])):
            embed.description= f"Unloading cog **{cog}** 🔄"
            embed = update_embed(embed)
            await msg.edit(embed= embed)

            self.bot.unload_extension(f"cogs.{cog}")
            prev_cogs.remove(cog)
            embed = update_embed(embed)
            embed.description= f"Cog **{cog}** unloaded, reloading 🔁"
            await msg.edit(embed= embed)

            self.bot.load_extension(f"cogs.{cog}")
            reloaded_cogs.append(cog)
            embed = update_embed(embed)
            embed.description= f"Cog **{cog}** reloaded ✅"
            await msg.edit(embed= embed)
        embed.description= f"Finished in {round(time.time()-_, 2)} secs ⌛"
        await msg.edit(embed= embed)
    

    # To-do list
    @commands.is_owner()
    @commands.command(hidden= True)
    async def todo(self, ctx, *, task):
        msg=await self.bot.get_channel(551203556896538627).send(embed= discord.Embed(
            title= "Added to the to-do list:", description= task,
            color= discord.Colour.blurple()))
        
        await ctx.send(embed= discord.Embed(title= "Added to the to-do list:", description= f"{task}\n\nView task [here]({msg.jump_url})", color= discord.Colour.blurple()))


    @commands.is_owner()
    @commands.command(hidden= True, aliases= ["guilds"])
    async def servers(self, ctx):
        msg= "**All servers**\n"
        for guild in self.bot.guilds: msg += f"{guild.name} - {guild.member_count} members\n"
        await ctx.send(msg)


    # Get command source
    @commands.is_owner()
    @commands.command(hidden= True)
    async def source(self, ctx, command):
        """Get the command source"""
        cmd = self.bot.get_command(command)
        if cmd is None: return await self.bot.send("", "Could not find that command :x:")
        await ctx.send(f"Here ya go\n```{getsource(ctx.callback)}```")
    

    @commands.is_owner()
    @commands.command(hidden= True)
    async def shutdown(self, ctx):
        """Shuts down the bot in an emergency, please be sure!"""
        if self.bot.user.id != 492873992982757406:
            await ctx.send(embed= discord.Embed(description= "Cya :wave:", color= r.randint(0, 0xFFFFFF)))
            await self.bot.logout()
            return

        try:
            embed= discord.Embed(description= "*really* shutdown the bot? (15 sec timeout)\n**Only for emergencies!!** (**not** sheer laziness)", color= r.randint(0, 0xFFFFFF))
            msg = await ctx.send(embed= embed)
            def check(reaction, user): return user == ctx.author and str(reaction.emoji) == "👍"
            await msg.add_reaction("👍")
            await self.bot.wait_for("reaction_add", timeout= 15.0, check= check)
        except:
            embed.description= "Timed out"
            await msg.edit(embed= embed)
            return await msg.remove_reaction("👍", self.bot.user)
        embed.description = "Cya! :wave:"
        await msg.edit(embed= embed)
        await self.bot.logout()

def setup(bot): bot.add_cog(Admin(bot))
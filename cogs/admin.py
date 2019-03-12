import json
import time
import inspect
import discord
import random as r
from setup import aiohttpget
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
    async def enable(self, ctx, command):
        try:
            cmd = self.bot.get_command(command)
            cmd.enabled= True
            await ctx.send(embed= discord.Embed(description= "Command enabled! ✅", color= r.randint(0, 0xFFFFFF)))
        except AttributeError: await ctx.send(embed= discord.Embed(description= "Command not found ❎"))


    @commands.is_owner()
    @commands.command(hidden= True)
    async def disable(self, ctx, command):
        try:
            cmd = self.bot.get_command(command)
            cmd.enabled= False
            await ctx.send(embed= discord.Embed(description= f"Command **{cmd}** disabled! ✅", color= r.randint(0, 0xFFFFFF)))
        except AttributeError: await ctx.send(embed= discord.Embed(description= "Command not found ❎"))


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
    @commands.group(hidden= True)
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed= discord.Embed(
                description= f"Use `{ctx.prefix}todo add <suggestion>` to add a task or `{ctx.prefix}todo list` to view the list",
                color= r.randint(0, 0xFFFFFF)))

    @todo.command()
    async def add(self, ctx, *, task):
        await ctx.trigger_typing()
        msg=await self.bot.get_channel(551203556896538627).send(embed= discord.Embed(
            title= "Added to the to-do list:", description= task,
            color= discord.Colour.blurple()))
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
        
        await ctx.send(embed= discord.Embed(title= "Added to the to-do list:", description= f"{task}\n\nView task [here]({msg.jump_url})", color= discord.Colour.blurple()))

    @todo.command(name= "list")
    async def _list(self, ctx):
        chnl, data = self.bot.get_channel(551203556896538627), []
        embed = discord.Embed(title= "To-do list", description= "", color= r.randint(0, 0xFFFFFF))

        async for msg in chnl.history():
            if msg.author.bot: # Some messages from me in there
                msg_data = {}
                msg_data["upvotes"] = 0

                msg_data["task"] = msg.embeds[0].description
                for reaction in msg.reactions:
                    if str(reaction.emoji) == "👍":
                        msg_data["upvotes"] += reaction.count
                    if str(reaction.emoji) == "👎":
                        msg_data["upvotes"] -= reaction.count
                
                data.append(msg_data)
        for task in sorted(data, key= lambda k: -k["upvotes"]):
            embed.description += f"{task['upvotes']} upvotes - **{task['task']}**\n\n"
        embed.set_footer(text= f"{len(data)} tasks on the to-do list")
        await ctx.send(embed= embed)


    # Check servers
    @commands.is_owner()
    @commands.command(hidden= True, aliases= ["guilds"])
    async def servers(self, ctx):
        """Get all the servers that the bot is in and how many members"""
        embed= discord.Embed(title= "**All servers**", description= "", color= r.randint(0, 0xFFFFFF))
        embed.set_footer(text= f"{len(list(self.bot.get_all_members()))} users across {len(self.bot.guilds)} servers")

        for guild in self.bot.guilds:
            embed.description += f"{guild.name} - {guild.member_count} members\n"
        
        await ctx.send(embed= embed)


    # Check last updates and commits
    @commands.is_owner()
    @commands.command(hidden= True)
    async def updates(self, ctx: commands.Context):
        """Get the most recent updates from GitHub (Move to public access?)"""
        await ctx.trigger_typing()

        embed= discord.Embed(title= "Last 5 updates", description= "", color= r.randint(0, 0xFFFFFF))
        data = json.loads(await aiohttpget("https://api.github.com/repos/aiden2480/savage-cabbage/commits?per_page=5"))
        _committer = data[0]["committer"]
        embed.set_author(name= _committer["login"], url= _committer["html_url"], icon_url= _committer["avatar_url"])

        for update in data:
            _cmt_date = update["commit"]["author"]["date"].replace("T", " ").replace("Z", "")
            _id = update["sha"][0:5]
            _url = update["html_url"]
            _desc = update["commit"]["message"]
            embed.description += f"**{_cmt_date}** - [`{_id}`]({_url}) {_desc}\n\n"
        
        await ctx.send(embed= embed)


    # Get command source
    @commands.is_owner()
    @commands.command(hidden= True)
    async def source(self, ctx, command):
        """Get the command source"""
        cmd = self.bot.get_command(command)
        if cmd is None: return await self.bot.send("", "Could not find that command ❎")
        await ctx.send(f"**Here ya go**```py\n{inspect.getsource(cmd.callback)}```")
    

    # Check which users have been banned
    @commands.is_owner()
    @commands.command(hidden= True, aliases= ["banlist"])
    async def botbans(self, ctx):
        embed= discord.Embed(title= "Bot bans", description= "", color= r.randint(0, 0xFFFFFF))
        for ban in self.bot.banlist:
            usr= await self.bot.get_user_info(ban[0])
            embed.description += f"{usr}, ID {ban[0]}. Banned for **{ban[1]}**\n\n"
        
        await ctx.send(embed= embed)

    # Shutdown the bot
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
import os
import time
import json
import discord
import requests
import webserver
import random as r
from setup import *
from discord.ext import commands


_runtime_ = time.time()
bot = commands.Bot(
    command_prefix= prefix,
    status= discord.Status.idle,
    owner_id= 272967064531238912,
    activity= discord.Game(name= "Restarting..."))


# Setup events
@bot.event
async def on_ready():
    """My async setup function"""

    bot.admins = [await bot.get_user_info(admin) for admin in [
        272967064531238912, # Me
        454928254558535700, # Dana
        297229962971447297, # Jack
    ]]


    bot.commands_run, bot.non_admin_commands_run, bot.initial_cogs = 0, 0, [
        "general", "fun", "currency",
        "memey", "text", "admin", "imagecog", "config"
    ]
    

    # bot.remove_command("help")
    bot.no_bypass_cooldown_commands = ["daily"]
    for cog in bot.initial_cogs:
        try: bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            print(f"Could not load cog {cog}: {e}")
            await bot.get_channel(546570094449393665).send(f"{bot.admins[0].mention}, cog **{cog}** could not be loaded", embed= discord.Embed(description= f"```py\n{e}```", color= r.randint(0, 0xFFFFFF)))


    bot.current_status = await change_status(bot)
    bot.serverprefixes = json.loads(requests.get(os.getenv("DATABASE_URL")+"/server-prefixes").text)["result"] # Change from requests though this first time might be ok
    print(f"Logged in as {bot.user} - {len(list(bot.get_all_members()))} users across {len(bot.guilds)} guilds - Loaded in {round(time.time()- _runtime_, 2)} seconds")
    if bot.user.id == 492873992982757406: await bot.get_channel(542961329867063326).send(embed= discord.Embed(title= "Bot restarted", description= f"Loaded in {round(time.time()- _runtime_, 2)} seconds\n\nRestarted: {get_time()}", color= 0x00BFFF))


# Guild events
@bot.event
async def on_guild_join(guild):
    """Log joining a guild"""
    
    embed = discord.Embed(
        title= "Guild join",
        color= 0x228B22,
        description= f"Joined **{guild.name}** (**{guild.member_count- 1}** other members)")
    
    embed.set_thumbnail(url= guild.icon_url)
    embed.add_field(name= "Guild Members", value= guild.member_count)
    embed.add_field(name= "New Total Guilds", value= len(bot.guilds))

    await bot.get_channel(542474215282966549).send(embed= embed)

@bot.event
async def on_guild_remove(guild):
    """Log leaving a guild"""
    
    embed = discord.Embed(
        title= "Kicked from guild",
        color= 0xf44e42,
        description= f"Kicked from **{guild.name}** (**{guild.member_count- 1}** other members)")
    
    embed.set_thumbnail(url= guild.icon_url)
    embed.add_field(name= "Guild Members", value= guild.member_count)
    embed.add_field(name= "New Total Guilds", value= len(bot.guilds))

    await bot.get_channel(542474215282966549).send(embed= embed)


# Message events
@bot.before_invoke
async def before_invoke(ctx):
    """Setup command-based refreshing data"""
    bot.send = SendEmbed(ctx).Send

@bot.event
async def on_command(ctx):
    """Log commands run"""
    
    embed = discord.Embed(title= "Command run", description= f"```{ctx.message.content}```", color= 0xf9e236)
    embed.add_field(name= "User", value= ctx.author)
    embed.add_field(name= "Channel", value= ctx.channel)
    embed.add_field(name= "Guild", value= ctx.guild)
    if ctx.guild: embed.set_thumbnail(url= ctx.guild.icon_url)
    embed.set_footer(text= ctx.author, icon_url= ctx.author.avatar_url)
    await bot.get_channel(542961329867063326).send(embed= embed)

    bot.commands_run += 1
    print(f"Command run: {ctx.author}: {ctx.message.content}")
    if ctx.author not in bot.admins: bot.non_admin_commands_run += 1

@bot.event
async def on_message(m):
    if m.author == bot.user: return
    #if m.author.id in bot.database["banlist"]: return

    if m.content == "no u": await m.channel.send("no u")

    await bot.process_commands(m)


# Error events
@bot.event
async def on_command_error(ctx, error):
    """Handle errors"""
    
    embed = discord.Embed(color = r.randint(0, 0xFFFFFF))
    ignored_errors = (commands.NotOwner)
    missing_param_errors = (commands.MissingRequiredArgument, commands.BadArgument, commands.TooManyArguments, commands.UserInputError)
    

    if isinstance(error, ignored_errors):
        pass
    elif isinstance(error, missing_param_errors):
        await ctx.send(embed= discord.Embed(
            color= r.randint(0, 0xFFFFFF),
            title= "Incorrect usage of command",
            description= f"{str(error)}\n\nThis is the correct usage: **{ctx.prefix}{ctx.command.signature}**"
        ))
    elif isinstance(error, commands.CommandNotFound):
        if ctx.guild != None: # DM commands don't need prefix
            await ctx.send(f"thats not a command lol {emojis.partyparrot}")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("oof, this is a `guild-only` command!")
    elif isinstance(error, commands.CommandOnCooldown):
        if user_in_support_guild(bot, ctx.message.author):
            if ctx.command.name not in bot.no_bypass_cooldown_commands: return await ctx.reinvoke()
            else: embed.title, embed.description= "Slow it down, cmon thats not fair", str(error)
        
        else: embed.title, embed.description= "Slow it down, cmon thats not fair", f"{str(error)}\n\n[Join the support guild]({SUPPORT_GUILD_INVITE}) and you won't have to wait!"
        await ctx.send(embed= embed)
    else:
        embed.title, embed.color= f"An error occoured", 0xFF8C00
        embed.description= f"**Traceback:**\n```py\n{format_error(error)}```"

        em= discord.Embed(
            color= 0xFFA500,
            title= "💣 Oof, an error occoured 💥",
            description= f"Please [join the support guild]({SUPPORT_GUILD_INVITE}) and tell **{bot.admins[0]}** what happened to help fix this bug")
        em.set_footer(text= "< Look for this guy!", icon_url= bot.admins[0].avatar_url)
        
        
        if ctx.author == bot.admins[0] and ctx.guild is None:
            await ctx.send(embed= embed)
        else:
            await bot.get_channel(546570094449393665).send(embed= embed)
            await ctx.send(embed= em)


webserver.start_server() # Implement bot in here too somehow
bot.run(os.getenv("BOT_TOKEN"))